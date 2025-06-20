"""show_dot1x.py
   supported commands:
     *  show dot1x
     *  show dot1x all details
     *  show dot1x all statistics
     *  show dot1x all summary
     *  show dot1x statistics
"""
# Python
import re

# Metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Schema, \
                                         Any, \
                                         Optional, \
                                         Or, \
                                         And, \
                                         Default, \
                                         Use

# import parser utils
from genie.libs.parser.utils.common import Common

# ====================================
# Parser for 'show dot1x all details'
# ====================================
class ShowDot1xAllDetailSchema(MetaParser):
    """Schema for show dot1x all details"""
    schema = {
        Optional('system_auth_control'): bool,
        Optional('version'): int,
        Optional('interfaces'): {
            Any(): {
                'pae': str,
                'interface': str,
                Optional('credentials'): str,
                Optional('port_control'): str,
                Optional('control_direction'): str,
                Optional('host_mode'): str,
                Optional('re_authentication'): bool,
                Optional('max_reauth_req'): int,
                Optional('max_req'): int,
                Optional('max_start'): int,
                Optional('timeout'): {
                    Optional('server_timeout'): int,
                    Optional('supp_timeout'): int,
                    Optional('quiet_period'): int,
                    Optional('tx_period'): int,
                    Optional('auth_period'): int,
                    Optional('held_period'): int,
                    Optional('ratelimit_period'): int,
                    Optional('start_period'): int,
                    Optional('re_auth_period'): int
                },
                Optional('authenticator'): {
                    'eap': {
                        'profile': str,
                    }
                },
                Optional('supplicant'): {
                    'eap': {
                        'profile': str,
                    }
                },
                Optional('clients'): {
                    Any(): {
                        'client': str,
                        'eap_method': str,
                        Optional('session'): {
                            Any(): {
                                'session_id': str,
                                'auth_sm_state': str,
                                'auth_bend_sm_state': str,
                            }
                        }
                    }
                }
            }
        }
    }


class ShowDot1xAllDetail(ShowDot1xAllDetailSchema):
    """Parser for show dot1x all details"""

    cli_command = 'show dot1x all details'

    def cli(self,output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        # initial return dictionary
        ret_dict = {}

        # initial regexp pattern
        p1 = re.compile(r'^Sysauthcontrol +(?P<val>\w+)$')
        p2 = re.compile(r'^Dot1x +Protocol +Version +(?P<val>\d+)$')
        p3 = re.compile(r'^Dot1x +Info +for +(?P<intf>[\w\-\/]+)$')
        p4 = re.compile(r'^(?P<key>[\w\s]+) +\= +(?P<val>[\w\-]+)( *[\(\)\s\w]+)?$')
        p5 = re.compile(r'^EAP +Method +\= +(?P<eap>\S+)$')
        p6 = re.compile(r'^Supplicant +\= +(?P<client>[\w\.]+)$')
        p7 = re.compile(r'^Session +ID +\= +(?P<session_id>[\w\-]+)$')
        p8 = re.compile(r'^Auth +SM +State +\= +(?P<state>[\w\-]+)$')
        p9 = re.compile(r'^Auth +BEND +SM +State +\= +(?P<state>[\w\-]+)$')

        for line in out.splitlines():
            line = line.strip()
            line = line.replace('\t', '    ')
            
            # Sysauthcontrol                 Enabled
            m = p1.match(line)
            if m:
                status = m.groupdict()['val'].lower()
                ret_dict['system_auth_control'] = True if 'enabled' in status else False
                continue

            # Dot1x Protocol Version               3
            m = p2.match(line)
            if m:
                ret_dict['version'] = int(m.groupdict()['val'])
                continue

            # Dot1x Info for GigabitEthernet1/0/9
            m = p3.match(line)
            if m:
                intf = m.groupdict()['intf']
                intf_dict = ret_dict.setdefault('interfaces', {}).setdefault(intf, {})
                intf_dict['interface'] = intf
                continue

            # EAP Method                = MD5
            m = p5.match(line)
            if m:
                eap_method = m.groupdict()['eap'].lower()
                continue

            # Supplicant                = fa16.3eff.c0c3
            m = p6.match(line)
            if m:
                client = m.groupdict()['client']
                client_dict = intf_dict.setdefault('clients', {}).setdefault(client, {})
                client_dict['client'] = client
                try:
                    client_dict['eap_method'] = eap_method
                except NameError:
                    pass
                continue

            # Session ID                = 000000000000000E00110F79
            m = p7.match(line)
            if m:
                session_id = m.groupdict()['session_id']
                sess_dict = client_dict.setdefault('session', {}).setdefault(session_id, {})
                sess_dict['session_id'] = session_id
                continue

            # Auth SM State         = HELD
            m = p8.match(line)
            if m:
                try:
                    sess_dict['auth_sm_state'] = m.groupdict()['state'].lower()
                except Exception:
                    pass
                continue

            # Auth BEND SM State    = IDLE
            m = p9.match(line)
            if m:
                try:
                    sess_dict['auth_bend_sm_state'] = m.groupdict()['state'].lower()
                except Exception:
                    pass
                continue

            m = p4.match(line)
            if m:
                group = m.groupdict()
                key = group['key']
                if 'PAE' in key:
                    # PAE                       = AUTHENTICATOR
                    intf_dict['pae'] = group['val'].lower()
                elif 'QuietPeriod' in key:
                    # QuietPeriod               = 60
                    intf_dict.setdefault('timeout', {})\
                        .setdefault('quiet_period', int(group['val']))
                elif 'ServerTimeout' in key:
                    # ServerTimeout             = 0
                    intf_dict.setdefault('timeout', {})\
                        .setdefault('server_timeout', int(group['val']))
                elif 'SuppTimeout' in key:
                    # SuppTimeout               = 30
                    intf_dict.setdefault('timeout', {})\
                        .setdefault('supp_timeout', int(group['val']))
                elif 'ReAuthMax' in key:
                    # ReAuthMax                 = 2
                    intf_dict['max_reauth_req'] = int(group['val'])
                elif 'MaxReq' in key:
                    # MaxReq                    = 2
                    intf_dict['max_req'] = int(group['val'])
                elif 'TxPeriod' in key:
                    # TxPeriod                  = 30
                    intf_dict.setdefault('timeout', {})\
                        .setdefault('tx_period', int(group['val']))
                elif 'StartPeriod' in key:
                    # StartPeriod               = 30
                    intf_dict.setdefault('timeout', {})\
                        .setdefault('start_period', int(group['val']))
                elif 'AuthPeriod' in key:
                    # AuthPeriod                = 30
                    intf_dict.setdefault('timeout', {})\
                        .setdefault('auth_period', int(group['val']))
                elif 'HeldPeriod' in key:
                    # HeldPeriod                = 60
                    intf_dict.setdefault('timeout', {})\
                        .setdefault('held_period', int(group['val']))
                elif 'MaxStart' in key:
                    # MaxStart                  = 3
                    intf_dict['max_start'] = int(group['val'])
                elif 'Credentials profile' in key:
                    # Credentials profile       = switch4
                    intf_dict['credentials'] = group['val']
                elif 'EAP profile' in key:
                    # EAP profile               = EAP-METH
                    if 'pae' in intf_dict:
                        intf_prof_dict = intf_dict.setdefault(intf_dict['pae'], {})\
                            .setdefault('eap', {})
                    intf_prof_dict['profile'] = group['val']
                elif 'PortControl' in key:
                    # PortControl               = AUTO
                    intf_dict['port_control'] = group['val'].lower()
                elif 'ControlDirection' in key:
                    # ControlDirection          = Both
                    intf_dict['control_direction'] = group['val'].lower()
                elif 'HostMode' in key:
                    # HostMode                  = SINGLE_HOST
                    intf_dict['host_mode'] = group['val'].lower()
                elif 'ReAuthentication' in key:
                    # ReAuthentication          = Disabled
                    intf_dict['re_authentication'] = False if 'disabled' \
                        in group['val'].lower() else True
                elif 'ReAuthPeriod' in key:
                    # ReAuthPeriod              = 3600 (Locally configured)
                    intf_dict.setdefault('timeout', {})\
                        .setdefault('re_auth_period', int(group['val']))
                elif 'RateLimitPeriod' in key:
                    # RateLimitPeriod           = 0
                    intf_dict.setdefault('timeout', {})\
                        .setdefault('ratelimit_period', int(group['val']))
                continue

        return ret_dict


# ====================================
# Parser for 'show dot1x'
# ====================================
class ShowDot1xSchema(MetaParser):
    """Schema for show dot1x"""
    schema = {
        'system_auth_control': bool,
        'version': int,
    }

class ShowDot1x(ShowDot1xAllDetail, ShowDot1xSchema):
    """Parser for show dot1x"""

    cli_command = 'show dot1x'


# ======================================
# Parser for 'show dot1x all statistics'
# ======================================
class ShowDot1xAllStatisticsSchema(MetaParser):
    """Schema for show dot1x all statistics"""
    schema = {
        'interfaces': {
            Any(): {
                'interface': str,
                'statistics': {
                    'rxinvalid': int,
                    'rxlenerr': int,
                    'rxtotal': int,
                    'txtotal': int,
                    'rxversion': int,
                    'lastrxsrcmac': str,
                    Optional('rxreq'): int,
                    Optional('txreq'): int,
                    Optional('txstart'): int,
                    Optional('rxstart'): int,
                    Optional('txlogoff'): int,
                    Optional('rxlogoff'): int,
                    Optional('txresp'): int,
                    Optional('rxresp'): int,
                    Optional('rxrespid'): int,
                    Optional('txreqid'): int,
                },
            }
        }
    }


class ShowDot1xAllStatistics(ShowDot1xAllStatisticsSchema):
    """Parser for show dot1x all statistics"""

    cli_command = 'show dot1x all statistics'

    def cli(self,output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output
        # initial return dictionary
        ret_dict = {}

        # initial regexp pattern
        p1 = re.compile(r'^Dot1x +(Supplicant|Authenticator) +Port +Statistics +for +(?P<intf>[\w\-\/]+)$')
        p2 = re.compile(r'^RxVersion +\= *(?P<rxversion>\d+) +'
                         r'LastRxSrcMAC +\= *(?P<lastrxsrcmac>\w+\.\w+\.\w+)$')
        p3 = re.compile(r'(\w+) +\= *(\d+)')

        for line in out.splitlines():
            line = line.strip()

            # remove tab, replace with space
            line = line.replace('\t', ' ')
            
            # Dot1x Supplicant Port Statistics for GigabitEthernet1/0/9
            # Dot1x Authenticator Port Statistics for GigabitEthernet0/1
            m = p1.match(line)
            if m:
                intf = m.groupdict()['intf']
                ret_dict.setdefault('interfaces', {}).setdefault(intf, {})\
                    .setdefault('interface', intf)
                stat_dict = ret_dict.setdefault('interfaces', {}).setdefault(intf, {})\
                    .setdefault('statistics', {})
                continue

            # RxVersion = 0   LastRxSrcMAC = 0000.0000.0000
            m = p2.match(line)
            if m:
                stat_dict['rxversion'] = int(m.groupdict()['rxversion'])
                stat_dict['lastrxsrcmac'] = m.groupdict()['lastrxsrcmac']
                continue

            # RxReq = 0       RxInvalid = 0    RxLenErr = 0    RxTotal = 0
            # TxStart = 3     TxLogoff = 0      TxResp = 0      TxTotal = 3
            m = p3.findall(line)
            if m:
                for item in m:
                    stat_dict.update({item[0].lower(): int(item[1])})
                continue

        return ret_dict


# ======================================
# Parser for 'show dot1x all summary'
# ======================================
class ShowDot1xAllSummarySchema(MetaParser):
    """Schema for show dot1x all summary"""
    schema = {
        'interfaces': {
            Any(): {
                'interface': str,
                'clients': {
                     Any(): {
                        'client': str,
                        'status': str,
                        'pae': str,
                    }
               }
            }
        }   
    }


class ShowDot1xAllSummary(ShowDot1xAllSummarySchema):
    """Parser for show dot1x all summary"""

    cli_command= 'show dot1x all summary'

    def cli(self,output=None):
        if output is None:
            # get output from device
            out = self.device.execute(self.cli_command)
        else:
            out = output

        # initial return dictionary
        ret_dict = {}

        # initial regexp pattern
        p1 = re.compile(r'^(?P<intf>[\w\-\/]+) +(?P<pae>\w+) +'
                         r'(?P<client>\w+\.\w+\.\w+) +(?P<status>\w+)$')
        p2 = re.compile(r'^((?P<pae>\w+) +)?(?P<client>\w+\.\w+\.\w+) +(?P<status>\w+)$')

        for line in out.splitlines():
            line = line.strip()
            line = line.replace('\t', '    ')
            
            # Fa1                   AUTH             000d.bcff.afcc           UNAUTHORIZED
            m = p1.match(line)
            if m:
                group = m.groupdict()
                intf = Common.convert_intf_name(group['intf'])
                intf_dict = ret_dict.setdefault('interfaces', {}).setdefault(intf, {})
                intf_dict['interface'] = intf

                client = group['client']
                client_dict = intf_dict.setdefault('clients', {}).setdefault(client, {})
                client_dict['client'] = client
                client_dict['status'] = group['status'].lower()
                client_dict['pae'] = 'authenticator' if 'auth' in group['pae'].lower() else 'supplicant'
                continue

            #                                        fa16.3eff.0ce0           AUTHORIZED
            #                       AUTH             000d.bcff.afcc           UNAUTHORIZED
            m = p2.match(line)
            if m:
                group = m.groupdict()
                pae = group['pae']
                pae = pae if pae else client_dict['pae']
                client = group['client']
                client_dict = intf_dict.setdefault('clients', {}).setdefault(client, {})
                client_dict.setdefault('pae', 
                    'authenticator' if 'auth' in pae.lower() else 'supplicant') if pae else None
                try:
                    client_dict['client'] = group['client']
                    client_dict['status'] = group['status'].lower()
                except Exception:
                    pass
                continue

        return ret_dict


# ======================================
# Parser for 'show dot1x all count'
# ======================================
class ShowDot1xAllCountSchema(MetaParser):
    """Schema for show dot1x all count"""
    schema = {
        'sessions': {
            'authorized_clients': int,
            'unauthorized_clients': int,
            'total': int,
        },  
    }


class ShowDot1xAllCount(ShowDot1xAllCountSchema):
    """Parser for show dot1x all count"""

    cli_command = 'show dot1x all count'

    def cli(self,output=None):
        if output is None:
            # get output from device
            out = self.device.execute(self.cli_command)
        else:
            out = output

        # initial return dictionary
        ret_dict = {}

        # initial regexp pattern
        p1 = re.compile(r'^Authorized +Clients +\= +(?P<authorized_clients>\d+)$')
        p2 = re.compile(r'^UnAuthorized +Clients +\= +(?P<unauthorized_clients>\d+)$')
        p3 = re.compile(r'^Total +No +of +Client +\= +(?P<total>\d+)$')

        for line in out.splitlines():
            line = line.strip()
            line = line.replace('\t', '    ')
            
            # Authorized Clients        = 0
            m = p1.match(line)
            if m:
                ret_dict.setdefault('sessions', {})['authorized_clients'] = \
                    int(m.groupdict()['authorized_clients'])
                continue

            # UnAuthorized Clients        = 0
            m = p2.match(line)
            if m:
                ret_dict.setdefault('sessions', {})['unauthorized_clients'] = \
                    int(m.groupdict()['unauthorized_clients'])
                continue

            # Total No of Client        = 0
            m = p3.match(line)
            if m:
                ret_dict.setdefault('sessions', {})['total'] = \
                    int(m.groupdict()['total'])
                continue
        return ret_dict


# ======================================================
# Schema for 'show dot1x statistics '
# ======================================================

class ShowDot1xStatisticsSchema(MetaParser):
    """Schema for show dot1x statistics"""

    schema = {
        'dot1x_stats': {
            'rx_start': int,
            'rx_logoff': int,
            'rx_resp': int,
            'rx_resp_id': int,
            'rx_req': int,
            'rx_invalid': int,
            'rx_len_err': int,
            'rx_total': int,
            'tx_start': int,
            'tx_logoff': int,
            'tx_resp': int,
            'tx_req': int,
            're_tx_req': int,
            're_tx_req_fail': int,
            'tx_req_id': int,
            're_tx_req_id': int,
            're_tx_req_id_fail': int,
            'tx_total': int,
        },
    }

# ======================================================
# Parser for 'show dot1x statistics '
# ======================================================
class ShowDot1xStatistics(ShowDot1xStatisticsSchema):
    """Parser for show dot1x statistics"""

    cli_command = 'show dot1x statistics'

    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)

        # RxStart = 2     RxLogoff = 0    RxResp = 14      RxRespID = 32
        p1 = re.compile(r"^RxStart\s+=\s+(?P<rx_start>\d+)\s+RxLogoff\s+=\s+(?P<rx_logoff>\d+)\s+RxResp\s+=\s+(?P<rx_resp>\d+)\s+RxRespID\s+=\s+(?P<rx_resp_id>\d+)$")
        # RxReq = 0       RxInvalid = 0   RxLenErr = 0
        p1_1 = re.compile(r"^RxReq\s+=\s+(?P<rx_req>\d+)\s+RxInvalid\s+=\s+(?P<rx_invalid>\d+)\s+RxLenErr\s+=\s+(?P<rx_len_err>\d+)$")
        # RxTotal = 53
        p1_2 = re.compile(r"^RxTotal\s+=\s+(?P<rx_total>\d+)$")
        # TxStart = 0     TxLogoff = 0    TxResp = 0
        p1_3 = re.compile(r"^TxStart\s+=\s+(?P<tx_start>\d+)\s+TxLogoff\s+=\s+(?P<tx_logoff>\d+)\s+TxResp\s+=\s+(?P<tx_resp>\d+)$")
        # TxReq = 16       ReTxReq = 0     ReTxReqFail = 0
        p1_4 = re.compile(r"^TxReq\s+=\s+(?P<tx_req>\d+)\s+ReTxReq\s+=\s+(?P<re_tx_req>\d+)\s+ReTxReqFail\s+=\s+(?P<re_tx_req_fail>\d+)$")
        # TxReqID = 36         ReTxReqID = 2       ReTxReqIDFail = 0
        p1_5 = re.compile(r"^TxReqID\s+=\s+(?P<tx_req_id>\d+)\s+ReTxReqID\s+=\s+(?P<re_tx_req_id>\d+)\s+ReTxReqIDFail\s+=\s+(?P<re_tx_req_id_fail>\d+)$")
        # TxTotal = 81
        p1_6 = re.compile(r"^TxTotal\s+=\s+(?P<tx_total>\d+)$")

        ret_dict = {}

        for line in output.splitlines():

            # RxStart = 2     RxLogoff = 0    RxResp = 14      RxRespID = 32
            match_obj = p1.match(line)
            if match_obj:
                dict_val = match_obj.groupdict()
                if 'dot1x_stats' not in ret_dict:
                    dot1x_stats = ret_dict.setdefault('dot1x_stats', {})
                dot1x_stats['rx_start'] = int(dict_val['rx_start'])
                dot1x_stats['rx_logoff'] = int(dict_val['rx_logoff'])
                dot1x_stats['rx_resp'] = int(dict_val['rx_resp'])
                dot1x_stats['rx_resp_id'] = int(dict_val['rx_resp_id'])
                continue

            # RxReq = 0       RxInvalid = 0   RxLenErr = 0
            match_obj = p1_1.match(line)
            if match_obj:
                dict_val = match_obj.groupdict()
                if 'dot1x_stats' not in ret_dict:
                    dot1x_stats = ret_dict.setdefault('dot1x_stats', {})
                dot1x_stats['rx_req'] = int(dict_val['rx_req'])
                dot1x_stats['rx_invalid'] = int(dict_val['rx_invalid'])
                dot1x_stats['rx_len_err'] = int(dict_val['rx_len_err'])
                continue

            # RxTotal = 53
            match_obj = p1_2.match(line)
            if match_obj:
                dict_val = match_obj.groupdict()
                if 'dot1x_stats' not in ret_dict:
                    dot1x_stats = ret_dict.setdefault('dot1x_stats', {})
                dot1x_stats['rx_total'] = int(dict_val['rx_total'])
                continue

            # TxStart = 0     TxLogoff = 0    TxResp = 0
            match_obj = p1_3.match(line)
            if match_obj:
                dict_val = match_obj.groupdict()
                if 'dot1x_stats' not in ret_dict:
                    dot1x_stats = ret_dict.setdefault('dot1x_stats', {})
                dot1x_stats['tx_start'] = int(dict_val['tx_start'])
                dot1x_stats['tx_logoff'] = int(dict_val['tx_logoff'])
                dot1x_stats['tx_resp'] = int(dict_val['tx_resp'])
                continue

            # TxReq = 16       ReTxReq = 0     ReTxReqFail = 0
            match_obj = p1_4.match(line)
            if match_obj:
                dict_val = match_obj.groupdict()
                if 'dot1x_stats' not in ret_dict:
                    dot1x_stats = ret_dict.setdefault('dot1x_stats', {})
                dot1x_stats['tx_req'] = int(dict_val['tx_req'])
                dot1x_stats['re_tx_req'] = int(dict_val['re_tx_req'])
                dot1x_stats['re_tx_req_fail'] = int(dict_val['re_tx_req_fail'])
                continue

            # TxReqID = 36         ReTxReqID = 2       ReTxReqIDFail = 0
            match_obj = p1_5.match(line)
            if match_obj:
                dict_val = match_obj.groupdict()
                if 'dot1x_stats' not in ret_dict:
                    dot1x_stats = ret_dict.setdefault('dot1x_stats', {})
                dot1x_stats['tx_req_id'] = int(dict_val['tx_req_id'])
                dot1x_stats['re_tx_req_id'] = int(dict_val['re_tx_req_id'])
                dot1x_stats['re_tx_req_id_fail'] = int(dict_val['re_tx_req_id_fail'])
                continue

            # TxTotal = 81
            match_obj = p1_6.match(line)
            if match_obj:
                dict_val = match_obj.groupdict()
                if 'dot1x_stats' not in ret_dict:
                    dot1x_stats = ret_dict.setdefault('dot1x_stats', {})
                dot1x_stats['tx_total'] = int(dict_val['tx_total'])
                continue


        return ret_dict

# ======================================
# Parser for 'show dot1x interface {interface} statistics'
# ======================================
class ShowDot1xInterfaceStatisticsSchema(MetaParser):
    """Schema for show dot1x interface statistics"""
    schema = {
        'interface': {
            Any(): {
                'type': {
                    Any():{
                        'rxtotal':int,
                        'txtotal':int,
                        'rxversion':int,
                        'lastrxsrcmac':str,
                        Optional('rxreq'): int,
                        Optional('rxlenerr'):int,
                        Optional('txstart'):int,
                        Optional('txlogoff'):int,
                        Optional('txresp'):int,
                        Optional('rxlogoff'):int,
                        Optional('rxstart'): int,
                        Optional('rxresp'):int,
                        Optional('rxrespid'):int,
                        Optional('rxinvalid'):int,
                        Optional('txreq'):int,
                        Optional('txreqid'):int,
                    },
                },
            },
        },
    }

class ShowDot1xInterfaceStatistics(ShowDot1xInterfaceStatisticsSchema):
    """Parser for show dot1x Interface Statistics"""

    cli_command= 'show dot1x interface {interface} statistics'

    def cli(self, interface, output=None):
        if output is None:
            output = self.device.execute(self.cli_command.format(interface=interface))

        # initial return dictionary
        result_dict = {}

        # Dot1x Authenticator Port Statistics for FortyGigabitEthernet1/1/1
        # Dot1x Supplicant Port Statistics for FortyGigabitEthernet1/1/1
        p1 = re.compile(r'^(Dot1x\s+(?P<type>[\w]+)+\s+Port\s+Statistics\s+for\s+(?P<interface>[\w\d\/]+))$')

        # RxStart = 0 RxLogoff = 0 RxResp = 3 RxRespID = 1
        p2 = re.compile(r'^(RxStart\s+=+\s+(?P<rxstart>[\d]+)+\s+RxLogoff\s+=+\s+(?P<rxlogoff>[\d]+)+\s+RxResp\s+=+\s+(?P<rxresp>[\d]+)+\s+RxRespID+\s+=+\s+(?P<rxrespid>[\d]+))$')

        # RxInvalid = 0 RxLenErr = 0 RxTotal = 5
        p3 = re.compile(r'^(RxInvalid\s+=+\s+(?P<rxinvalid>[\d]+)+\s+RxLenErr\s+=+\s+(?P<rxlenerr>[\d]+)+\s+RxTotal\s+=+\s+(?P<rxtotal>[\d]+))$')

        # TxReq = 4 TxReqID = 1 TxTotal = 5
        p4 = re.compile(r'^(TxReq\s+=+\s+(?P<txreq>[\d]+)+\s+TxReqID\s+=+\s+(?P<txreqid>[\d]+)+\s+TxTotal\s+=+\s+(?P<txtotal>[\d]+))$')

        # RxVersion = 3 LastRxSrcMAC = 0027.90bf.c931
        # RxVersion = 0 LastRxSrcMAC = 0027.90bf.c931
        p5 = re.compile(r'^(RxVersion\s+=+\s+(?P<rxversion>[\d]+)+\s+LastRxSrcMAC\s+=+\s+(?P<lastrxsrcmac>\w+\.\w+\.\w+))$')

        # RxReq = 24 RxInvalid = 0 RxLenErr = 0 RxTotal = 28
        p6 = re.compile(r'^(RxReq\s+=+\s+(?P<rxreq>[\d]+)+\s+RxInvalid\s+=+\s+(?P<rxinvalid>[\d]+)+\s+RxLenErr\s+=+\s+(?P<rxlenerr>[\d]+)+\s+RxTotal\s+=+\s+(?P<rxtotal>[\d]+))$')

        # TxStart = 8 TxLogoff = 4 TxResp = 24 TxTotal = 36
        p7 = re.compile(r'^(TxStart\s+=+\s+(?P<txstart>[\d]+)+\s+TxLogoff\s+=+\s+(?P<txlogoff>[\d]+)+\s+TxResp\s+=+\s+(?P<txresp>[\d]+)+\s+TxTotal\s+=+\s+(?P<txtotal>[\d]+))$')

        for line in output.splitlines():
            line = line.strip()
            
            # Dot1x Authenticator Port Statistics for FortyGigabitEthernet1/1/1
            # Dot1x Supplicant Port Statistics for FortyGigabitEthernet1/1/1
            m = p1.match(line)
            if m:
                type_dict = result_dict.setdefault('interface', {}).setdefault(Common.convert_intf_name(m.groupdict()['interface']), {})
                object_type=m.groupdict()['type'].strip()
                ret_dict= type_dict.setdefault('type', {}).setdefault(object_type, {})
                continue
            
            # RxStart = 0 RxLogoff = 0 RxResp = 3 RxRespID = 1
            m = p2.match(line)
            if m:
                ret_dict['rxlogoff']=int(m.groupdict()['rxlogoff'])
                ret_dict['rxresp']=int(m.groupdict()['rxresp'])
                ret_dict['rxrespid']=int(m.groupdict()['rxrespid'])
                continue
        
            # RxInvalid = 0 RxLenErr = 0 RxTotal = 5
            m = p3.match(line)
            if m:  
                ret_dict['rxinvalid']=int(m.groupdict()['rxinvalid'])
                ret_dict['rxlenerr']=int(m.groupdict()['rxlenerr'])
                ret_dict['rxtotal']=int(m.groupdict()['rxtotal'])
                continue

            # TxReq = 4 TxReqID = 1 TxTotal = 5
            m = p4.match(line)
            if m:    
                ret_dict['txreq']=int(m.groupdict()['txreq'])
                ret_dict['txreqid']=int(m.groupdict()['txreqid'])
                ret_dict['txtotal']=int(m.groupdict()['txtotal'])
                continue
            # RxVersion = 3 LastRxSrcMAC = 0027.90bf.c931
            # RxVersion = 0 LastRxSrcMAC = 0027.90bf.c931
            m = p5.match(line)
            if m:    
                ret_dict['rxversion']=int(m.groupdict()['rxversion'])
                ret_dict['lastrxsrcmac']=m.groupdict()['lastrxsrcmac']
                continue
        
            # RxReq = 24 RxInvalid = 0 RxLenErr = 0 RxTotal = 28 
            m = p6.match(line)
            if m:    
                ret_dict['rxinvalid']=int(m.groupdict()['rxinvalid'])
                ret_dict['rxlenerr']=int(m.groupdict()['rxlenerr'])
                ret_dict['rxtotal']=int(m.groupdict()['rxtotal'])
                continue
        
            # TxStart = 8 TxLogoff = 4 TxResp = 24 TxTotal = 36
            m = p7.match(line)
            if m:    
                ret_dict['txstart']=int(m.groupdict()['txstart'])
                ret_dict['txlogoff']=int(m.groupdict()['txlogoff'])
                ret_dict['txresp']=int(m.groupdict()['txresp']) 
                ret_dict['txtotal']=int(m.groupdict()['txtotal'])
                continue

        return result_dict

class ShowParameterMapTypeSubscriberAttributeToServiceSchema(MetaParser):
    """Schema for show parameter-map type subscriber attribute-to-service name {template name}"""
    schema = {
        'parameter_map_name': str,
        'maps': {
            Any(): {
                'device_type': str,
                'action': {
                    Any(): {
                        'interface_template': str
                    }
                }
            }
        }
    }

class ShowParameterMapTypeSubscriberAttributeToService(ShowParameterMapTypeSubscriberAttributeToServiceSchema):
    """Parser for show parameter-map type subscriber attribute-to-service name {template name}"""

    cli_command = 'show parameter-map type subscriber attribute-to-service name {template_name}'

    def cli(self, template_name, output=None):
        if output is None:
            output = self.device.execute(self.cli_command.format(template_name=template_name))

        ret_dict = {}

        # Regex patterns
        # Parameter-map name: BUILTIN_DEVICE_TO_TEMPLATE
        p1 = re.compile(r'^Parameter-map +name: +(?P<parameter_map_name>\S+)$')
        
        # Map: 10 device-type regex "Cisco-IP-Phone"
        p2 = re.compile(r'^Map: +(?P<map_id>\d+) +device-type +regex +"(?P<device_type>.+)"$')
        
        # Map: 40 oui eq "00.0f.44"
        p3 = re.compile(r'^Map: +(?P<map_id>\d+) +oui +eq +"(?P<device_type>.+)"$')
        
        # 20 interface-template IP_PHONE_INTERFACE_TEMPLATE
        p4 = re.compile(r'^\d+ +interface-template +(?P<interface_template>\S+)$')

        current_map = None

        for line in output.splitlines():
            line = line.strip()

            # Parameter-map name: BUILTIN_DEVICE_TO_TEMPLATE
            m = p1.match(line)
            if m:
                ret_dict['parameter_map_name'] = m.groupdict()['parameter_map_name']
                continue

            # Map: 10 device-type regex "Cisco-IP-Phone"
            m = p2.match(line)
            if m:
                group = m.groupdict()
                current_map = int(group['map_id'])
                map_dict = ret_dict.setdefault('maps', {}).setdefault(current_map, {})
                map_dict['device_type'] = group['device_type']
                continue

            # Map: 40 oui eq "00.0f.44"
            m = p3.match(line)
            if m:
                group = m.groupdict()
                current_map = int(group['map_id'])
                map_dict = ret_dict.setdefault('maps', {}).setdefault(current_map, {})
                map_dict['device_type'] = group['device_type']
                continue

            # 20 interface-template IP_PHONE_INTERFACE_TEMPLATE
            m = p4.match(line)
            if m and current_map:
                action_id = int(line.split()[0])
                action_dict = ret_dict['maps'][current_map].setdefault('action', {}).setdefault(action_id, {})
                action_dict['interface_template'] = m.groupdict()['interface_template']
                continue

        return ret_dict