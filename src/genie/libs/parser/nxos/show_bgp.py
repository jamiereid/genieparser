"""show_bgp.py

NXOS parsers for the following show commands:
    * 'show bgp process vrf all'
    * 'show bgp process vrf all | xml'
    * 'show bgp peer-session <WORD>'
    * 'show bgp peer-policy <WORD>'
    * 'show bgp peer-template <WORD>'
    * 'show bgp all dampening flap-statistics'
    * 'show bgp all dampening flap-statistics | xml'
    * 'show bgp all nexthop-database'
    * 'show bgp all nexthop-database | xml'
    * 'show bgp peer-template'
    * 'show bgp peer-template | xml'
    * 'show bgp <address_family>  policy statistics redistribute'
    * 'show bgp <address_family>  policy statistics redistribute | xml'
    * 'show bgp <address_family>  policy statistics dampening'
    * 'show bgp <address_family>  policy statistics dampening | xml'
    * 'show bgp <address_family>  policy statistics neighbor <neighbor>'
    * 'show bgp <address_family>  policy statistics neighbor <neighbor> | xml'
    * 'show bgp sessions'
    * 'show bgp sessions | xml'
    * 'show bgp sessions vrf <WORD>'
    * 'show bgp sessions vrf <WORD> | xml'
    * 'show bgp <address_family>  labels vrf <WORD>'
    * 'show bgp <address_family>  labels vrf <WORD> | xml'
    * 'show bgp <address_family>  labels'
    * 'show bgp <address_family>  labels | xml'
    * 'show bgp l2vpn evpn summary'
    * 'show bgp l2vpn evpn route-type <route-type>'
    * 'show bgp l2vpn evpn route-type <route-type> vrf <vrf>'
    * 'show bgp l2vpn evpn <WORD> | be "best path, in rib" n <WORD>'

"""

# Python
import re
from copy import deepcopy
import xml.etree.ElementTree as ET

# Metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Schema, Any, Optional, Or, And,\
                                         Default, Use, ListOf

# Parser
from genie.libs.parser.yang.bgp_openconfig_yang import BgpOpenconfigYang
from genie.libs.parser.nxos.show_bgp_vrf import *

# import parser utils
from genie.libs.parser.utils.common import Common


# =====================================
# Schema for 'show bgp process vrf all'
# =====================================
class ShowBgpProcessVrfAllSchema(MetaParser):
    """Schema for show bgp process vrf all
                show bgp process vrf <vrf>"""

    schema = {
        Optional('bgp_pid'): int,
        Optional('bgp_protocol_started_reason'): str,
        Optional('bgp_performance_mode'): str,
        Optional('bgp_tag'): str,
        Optional('bgp_protocol_state'): str,
        Optional('bgp_isolate_mode'): str,
        Optional('bgp_mmode'): str,
        Optional('bgp_memory_state'): str,
        Optional('bgp_asformat'): str,
        Optional('segment_routing_global_block'): str,
        Optional('num_attr_entries'): int,
        Optional('hwm_attr_entries'): int,
        Optional('bytes_used'): int,
        Optional('entries_pending_delete'): int,
        Optional('hwm_entries_pending_delete'): int,
        Optional('bgp_paths_per_hwm_attr'): int,
        Optional('bgp_as_path_entries'): int,
        Optional('bytes_used_as_path_entries'): int,
        Optional('vrf'): 
            {Any(): 
                {'vrf_id': str,
                 'vrf_state': str,
                 Optional('vnid'): str,
                 Optional('topo_id'): str,
                 Optional('encap_type'): str,
                 Optional('vtep_ip'): str,
                 Optional('vtep_virtual_ip'): str,
                 Optional('vtep_vip_r'): str,
                 Optional('router_mac'): str,
                 Optional('vip_derived_mac'): str,
                 Optional('router_id'): str,
                 Optional('conf_router_id'): str,
                 Optional('confed_id'): int,
                 Optional('cluster_id'): str,
                 'num_conf_peers': int,
                 'num_pending_conf_peers': int,
                 'num_established_peers': int,
                 Optional('vrf_rd'): str,
                 Optional('vrf_evpn_rd'): str,
                 Optional('graceful_restart'): bool,
                 Optional('graceful_restart_helper_only'): bool,
                 Optional('graceful_restart_restart_time'): int,
                 Optional('graceful_restart_stalepath_time'): int,
                 Optional('address_family'): 
                    {Any(): 
                        {Optional('table_id'): str,
                         Optional('table_state'): str,
                         Optional('enabled'): bool,
                         Optional('graceful_restart'): bool,
                         Optional('advertise_inactive_routes'): bool,
                         Optional('ebgp_max_paths'): int,
                         Optional('ibgp_max_paths'): int,
                         Optional('total_paths'): int,
                         Optional('total_prefixes'): int,
                         Optional('peers'): 
                            {Any(): 
                                {'active_peers': int,
                                 'routes': int,
                                 'paths': int,
                                 'networks': int,
                                 'aggregates': int,
                                },
                            },
                         Optional('redistribution'): 
                            {Any(): 
                                {Optional('route_map'): str,
                                },
                            },
                         Optional('export_rt_list'): str,
                         Optional('import_rt_list'): str,
                         Optional('evpn_export_rt_list'): str,
                         Optional('evpn_import_rt_list'): str,
                         Optional('mvpn_export_rt_list'): str,
                         Optional('mvpn_import_rt_list'): str,
                         Optional('label_mode'): str,
                         Optional('aggregate_label'): str,
                         Optional('allocate_index'): str,
                         Optional('route_reflector'): bool,
                         Optional('next_hop_trigger_delay'):
                            {'critical': int,
                             'non_critical': int,
                            },
                        Optional('import_default_map'): str,
                        Optional('import_default_prefix_limit'): int,
                        Optional('import_default_prefix_count'): int,
                        Optional('export_default_map'): str,
                        Optional('export_default_prefix_limit'): int,
                        Optional('export_default_prefix_count'): int,
                        },
                    },
                },
            },
        }

# =====================================
# Parser for 'show bgp process vrf all'
# =====================================
class ShowBgpProcessVrfAll(ShowBgpProcessVrfAllSchema):
    """Parser for:
        show bgp process vrf all
        show bgp process vrf <vrf>
        parser class - implements detail parsing mechanisms for cli,xml and yang output.
    """
    cli_command = ['show bgp process vrf all', 'show bgp process vrf {vrf}']
    xml_command = ['show bgp process vrf all | xml', 'show bgp process vrf {vrf} | xml']
    exclude = [
      'bgp_pid',
      'hwm_attr_entries',
      'bgp_protocol_started_reason',
      'aggregate_label',
      'bgp_paths_per_hwm_attr',
      'bytes_used',
      'num_attr_entries',
      'router_id',
      'paths',
      'routes']

    def cli(self, vrf='', output=None):
        if vrf:
            cmd = self.cli_command[1].format(vrf=vrf)
        else:
            cmd = self.cli_command[0]
        if output is None:
            out = self.device.execute(cmd)
        else:
            out = output
        
        # Init vars
        parsed_dict = {}

        p1 = re.compile(r'^\s*BGP +Process +ID *: +(?P<bgp_pid>[0-9]+)$')
        p2 = re.compile(r'^\s*BGP Protocol Started, +reason: *:'
                            r' +(?P<reason>[a-zA-Z\s]+)$')
        p2_1 = re.compile(r'^\s*BGP +Performance +Mode: *:'
                            r' +(?P<performance_mode>[a-zA-Z\s]+)$')
        p3 = re.compile(r'^\s*BGP +Protocol +Tag *:'
                            r' +(?P<bgp_tag>[a-zA-Z0-9]+)$')
        p4 = re.compile(r'^\s*BGP +Protocol +State *:'
                            r' +(?P<protocol_state>[a-zA-Z\(\)\s]+)$')
        p4_1 = re.compile(r'^\s*BGP +Isolate +Mode *:'
                            r' +(?P<isolate_mode>[a-zA-Z\s]+)$')
        p4_3 = re.compile(r'^\s*BGP +MMODE *:'
                            r' +(?P<mmode>[a-zA-Z\s]+)$')
        p5 = re.compile(r'^\s*BGP +Memory +State *:'
                            r' +(?P<memory_state>[\w\s]+)$')
        p5_1 = re.compile(r'^\s*BGP +asformat *:'
                            r' +(?P<asformat>[a-zA-Z\s]+)$')
        p5_2 = re.compile(r'^\s*Segment +Routing +Global +Block *:'
                            r' +(?P<segment>[0-9\-]+)$')
        p6 = re.compile(r'^\s*Number +of +attribute +entries *:'
                            r' +(?P<num_attr_entries>[0-9]+)$')
        p7 = re.compile(r'^\s*HWM +of +attribute +entries *:'
                            r' +(?P<hwm_attr_entries>[0-9]+)$')
        p8 = re.compile(r'^\s*Bytes +used +by +entries *:'
                            r' +(?P<bytes_used>[0-9]+)$')
        p9 = re.compile(r'^\s*Entries +pending +delete *:'
                            r' +(?P<entries_pending_delete>[0-9]+)$')
        p10 = re.compile(r'^\s*HWM +of +entries +pending +delete *:'
                            r' +(?P<hwm_entries_pending_delete>[0-9]+)$')
        p11 = re.compile(r'^\s*BGP +paths +per +attribute +HWM *:'
                            r' +(?P<bgp_paths_per_hwm_attr>[0-9]+)$')
        p12 = re.compile(r'^\s*BGP +AS +path +entries *:'
                            r' +(?P<bgp_as_path_entries>[0-9]+)$')
        p13 = re.compile(r'^\s*Bytes +used +by +AS +path +entries *:'
                            r' +(?P<bytes_used_as_path_entries>[0-9]+)$')
        p14 = re.compile(r'^\s*BGP +Information +for +VRF'
                            r' +(?P<vrf_name>(\S+))$')
        p15 = re.compile(r'^\s*VRF +Id *:'
                            r' +(?P<vrf_id>[a-zA-Z0-9]+)$')
        p16 = re.compile(r'^\s*VRF +state *:'
                            r' +(?P<vrf_state>[a-zA-Z]+)$')
        p16_1 = re.compile(r'^\s*VNID *:'
                            r' +(?P<vnid>[a-zA-Z0-9]+)(?: +\((\S+)\))?$')
        p16_2 = re.compile(r'^\s*Topo +Id *: +(?P<topo_id>(\d+))$')
        p16_3 = re.compile(r'^\s*Encap +type *: +(?P<etype>(\S+))$')
        p16_4 = re.compile(r'^\s*VTEP +IP *: +(?P<vtep_ip>(\S+))$')
        p16_5 = re.compile(r'^\s*VTEP +Virtual +IP *: +(?P<vtep_vip>(\S+))$')
        p16_6 = re.compile(r'^\s*VTEP +VIP-R *: +(?P<vipr>(\S+))$')
        p16_7 = re.compile(r'^\s*Router-MAC *: +(?P<router_mac>(\S+))$')
        p16_8 = re.compile(r'^\s*VIP +Derived +MAC *: +(?P<vipd_mac>(\S+))$')
        p17 = re.compile(r'^\s*Router-ID *:'
                            r' +(?P<router_id>[0-9\.]+)$')
        p18 = re.compile(r'^\s*Configured +Router-ID *:'
                            r' +(?P<conf_router_id>[0-9\.]+)$')
        p19 = re.compile(r'^\s*Confed-ID *:'
                            r' +(?P<confed_id>[0-9]+)$')
        p20 = re.compile(r'^\s*Cluster-ID *:'
                            r' +(?P<cluster_id>[0-9\.]+)$')
        p21 = re.compile(r'^\s*No. +of +configured +peers *:'
                            r' +(?P<num_conf_peers>[0-9]+)$')
        p22 = re.compile(r'^\s*No. +of +pending +config +peers *:'
                            r' +(?P<num_pending_conf_peers>[0-9]+)$')
        p23 = re.compile(r'^\s*No. +of +established +peers *:'
                            r' +(?P<num_established_peers>[0-9]+)$')
        p24 = re.compile(r'^\s*VRF +RD *:'
                            r' +(?P<vrf_rd>[a-zA-Z0-9\:\.\s]+)$')
        p24_1 = re.compile(r'^\s*VRF +EVPN +RD *:'
                            r' +(?P<vrf_evpn_rd>[a-zA-Z0-9\:\.\s]+)$')
        p25 = re.compile(r'^\s*Information +for +address +family'
                            r' +(?P<address_family>[a-zA-Z0-9\s\-\_]+)'
                            r' +in +VRF +(?P<vrf>(\S+))$')
        p26 = re.compile(r'^\s*Table +Id *: +(?P<table_id>(\S+))$')
        p27 = re.compile(r'^\s*Table +state *: +(?P<table_state>[a-zA-Z]+)$')
        p28 = re.compile(r'^\s*(?P<peers>[0-9]+) +(?P<active_peers>[0-9]+)'
                            r' +(?P<routes>[0-9]+) +(?P<paths>[0-9]+)'
                            r' +(?P<networks>[0-9]+) +(?P<aggregates>[0-9]+)$')
        p29 = re.compile(r'^\s*(?P<name>[a-zA-Z]+),'
                            r' +route-map +(?P<route_map>[a-zA-Z0-9\-\_]+)$')
        p30 = re.compile(r'^\s*(?P<type>(Export|Import|EVPN Export|'
                            r'EVPN Import|MVPN Export|MVPN Import)) +RT +list'
                            r' *:(?: +(?P<rt_list>[0-9\:]+))?$')
        p31 = re.compile(r'^\s*(?P<rt_list>((\w+)\:(\d+))(\s+(\w+)\:(\d+))?)$')
        p32 = re.compile(r'^\s*Label +mode *: +(?P<label_mode>[a-zA-Z\-]+)$')
        p32_1 = re.compile(r'^\s*Is +a +Route\-reflector$')
        p33 = re.compile(r'^\s*Aggregate +label *:'
                            r' +(?P<aggregate_label>[a-zA-Z0-9\-]+)$')
        p33_1 = re.compile(r'^\s*Allocate-index *:'
                           r' +(?P<allocate_index>[a-zA-Z0-9\-]+)$')
        p34 = re.compile(r'^\s*Import +default +limit *:'
                            r' +(?P<import_default_prefix_limit>[0-9]+)$')
        p35 = re.compile(r'^\s*Import +default +prefix +count *:'
                            r' +(?P<import_default_prefix_count>[0-9]+)$')
        p36 = re.compile(r'^\s*Import +default +map *:'
                            r' +(?P<import_default_map>[a-zA-Z0-9\_\-]+)$')
        p37 = re.compile(r'^\s*Export +default +limit *:'
                            r' +(?P<export_default_prefix_limit>[0-9]+)$')
        p38 = re.compile(r'^\s*Export +default +prefix +count *:'
                            r' +(?P<export_default_prefix_count>[0-9]+)$')
        p39 = re.compile(r'^\s*Export +default +map *:'
                            r' +(?P<export_default_map>[a-zA-Z0-9\_\-]+)$')
        p40 = re.compile(r'^\s*Nexthop +trigger-delay$')
        p41 = re.compile(r'^\s*critical +(?P<critical>[0-9]+) +ms$')
        p42 = re.compile(r'^\s*non-critical +(?P<non_critical>[0-9]+) +ms$')


        for line in out.splitlines():
            line = line.replace('\t', '    ')
            line = line.rstrip()

            # BGP Process ID                 : 29474
            m = p1.match(line)
            if m:
                parsed_dict['bgp_pid'] = int(m.groupdict()['bgp_pid'])
                continue

            # BGP Protocol Started, reason:  : configuration
            m = p2.match(line)
            if m:
                parsed_dict['bgp_protocol_started_reason'] = \
                    str(m.groupdict()['reason']).lower()
                continue

            # BGP Performance Mode:          : No
            m = p2_1.match(line)
            if m:
                parsed_dict['bgp_performance_mode'] = \
                    str(m.groupdict()['performance_mode'])
                continue

            # BGP Protocol Tag               : 100
            m = p3.match(line)
            if m:
                parsed_dict['bgp_tag'] = str(m.groupdict()['bgp_tag']).lower()
                continue

            # BGP Protocol State             : Running
            m = p4.match(line)
            if m:
                parsed_dict['bgp_protocol_state'] = \
                    str(m.groupdict()['protocol_state']).lower()
                continue

            # BGP Isolate Mode               : No
            m = p4_1.match(line)
            if m:
                parsed_dict['bgp_isolate_mode'] = \
                    str(m.groupdict()['isolate_mode'])
                continue

            # BGP MMODE                      : Initialized
            m = p4_3.match(line)
            if m:
                parsed_dict['bgp_mmode'] = str(m.groupdict()['mmode'])
                continue

            # BGP Memory State               : OK
            # BGP Memory State               : Severe Alert
            m = p5.match(line)
            if m:
                parsed_dict['bgp_memory_state'] = \
                    str(m.groupdict()['memory_state']).lower()
                continue

            # BGP asformat                   : asplain
            m = p5_1.match(line)
            if m:
                parsed_dict['bgp_asformat'] = str(m.groupdict()['asformat'])
                continue

            # Segment Routing Global Block   : 10000-25000
            m = p5_2.match(line)
            if m:
                parsed_dict['segment_routing_global_block'] = \
                    str(m.groupdict()['segment'])
                continue

            # BGP attributes information
            # Number of attribute entries    : 4
            m = p6.match(line)
            if m:
                parsed_dict['num_attr_entries'] = \
                    int(m.groupdict()['num_attr_entries'])
                continue

            # HWM of attribute entries       : 5
            m = p7.match(line)
            if m:
                parsed_dict['hwm_attr_entries'] = \
                    int(m.groupdict()['hwm_attr_entries'])
                continue

            # Bytes used by entries          : 368
            m = p8.match(line)
            if m:
                parsed_dict['bytes_used'] = int(m.groupdict()['bytes_used'])
                continue

            # Entries pending delete         : 0
            m = p9.match(line)
            if m:
                parsed_dict['entries_pending_delete'] = \
                    int(m.groupdict()['entries_pending_delete'])
                continue

            # HWM of entries pending delete  : 0
            m = p10.match(line)
            if m:
                parsed_dict['hwm_entries_pending_delete'] = \
                    int(m.groupdict()['hwm_entries_pending_delete'])
                continue

            # BGP paths per attribute HWM    : 1
            m = p11.match(line)
            if m:
                parsed_dict['bgp_paths_per_hwm_attr'] = \
                    int(m.groupdict()['bgp_paths_per_hwm_attr'])
                continue

            # BGP AS path entries            : 0
            m = p12.match(line)
            if m:
                parsed_dict['bgp_as_path_entries'] = \
                    int(m.groupdict()['bgp_as_path_entries'])
                continue

            # Bytes used by AS path entries  : 0
            m = p13.match(line)
            if m:
                parsed_dict['bytes_used_as_path_entries'] = \
                    int(m.groupdict()['bytes_used_as_path_entries'])
                continue

            # BGP Information for VRF VRF1
            m = p14.match(line)
            if m:
                if 'vrf' not in parsed_dict:
                    parsed_dict['vrf'] = {}
                vrf_name = str(m.groupdict()['vrf_name'])
                if vrf_name not in parsed_dict['vrf']:
                    parsed_dict['vrf'][vrf_name] = {}
                    continue

            # VRF Id                         : 3
            m = p15.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['vrf_id'] = \
                    str(m.groupdict()['vrf_id'])
                continue

            # VRF state                      : UP
            m = p16.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['vrf_state'] = \
                    str(m.groupdict()['vrf_state']).lower()
                continue

            # VNID                           : 9105 (valid)
            m = p16_1.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['vnid'] = m.groupdict()['vnid']
                continue

            # Topo Id                        : 1005
            m = p16_2.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['topo_id'] = \
                    m.groupdict()['topo_id']
                continue

            # Encap type                     : VXLAN
            m = p16_3.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['encap_type'] = \
                    m.groupdict()['etype']
                continue

            # VTEP IP                        : 10.49.1.1
            m = p16_4.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['vtep_ip'] = \
                    m.groupdict()['vtep_ip']
                continue

            # VTEP Virtual IP                : 10.49.2.1
            m = p16_5.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['vtep_virtual_ip'] = \
                    m.groupdict()['vtep_vip']
                continue

            # VTEP VIP-R                     : 10.49.2.1
            m = p16_6.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['vtep_vip_r'] = \
                    m.groupdict()['vipr']
                continue

            # Router-MAC                     : 000c.29ff.a329
            m = p16_7.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['router_mac'] = \
                    m.groupdict()['router_mac']
                continue

            # VIP Derived MAC                : 000c.29ff.a329
            m = p16_8.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['vip_derived_mac'] = \
                    m.groupdict()['vipd_mac']
                continue

            # Router-ID                      : 10.229.11.11
            m = p17.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['router_id'] = \
                    str(m.groupdict()['router_id'])
                continue

            # Configured Router-ID           : 0.0.0.0
            m = p18.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['conf_router_id'] = \
                    str(m.groupdict()['conf_router_id'])
                continue

            # Confed-ID                      : 0
            m = p19.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['confed_id'] = \
                    int(m.groupdict()['confed_id'])
                continue

            # Cluster-ID                     : 0.0.0.0
            m = p20.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['cluster_id'] = \
                    str(m.groupdict()['cluster_id'])
                continue

            # No. of configured peers        : 1
            m = p21.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['num_conf_peers'] = \
                    int(m.groupdict()['num_conf_peers'])
                continue
            
            # No. of pending config peers    : 0
            m = p22.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['num_pending_conf_peers'] = \
                    int(m.groupdict()['num_pending_conf_peers'])
                continue
            
            # No. of established peers       : 0
            m = p23.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['num_established_peers'] = \
                    int(m.groupdict()['num_established_peers'])
                continue
            
            # VRF RD                         : 100:100
            # VRF RD                         : 10.49.1.0:4
            m = p24.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['vrf_rd'] = \
                    str(m.groupdict()['vrf_rd']).lower()
                continue

            # VRF EVPN RD                    : 100:100
            # VRF EVPN RD                    : 10.49.1.0:4
            m = p24_1.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['vrf_evpn_rd'] = \
                    str(m.groupdict()['vrf_evpn_rd']).lower()
                continue

            #     Information for address family IPv4 Unicast in VRF VRF1
            m = p25.match(line)
            if m:
                if 'address_family' not in parsed_dict['vrf'][vrf_name]:
                    parsed_dict['vrf'][vrf_name]['address_family'] = {}

                address_family = str(m.groupdict()['address_family']).lower()
                
                vrf = str(m.groupdict()['vrf'])

                if address_family not in parsed_dict['vrf'][vrf_name]\
                    ['address_family'] and vrf == vrf_name:
                    parsed_dict['vrf'][vrf_name]['address_family']\
                        [address_family] = {}
                    # Init export/import RT variables
                    export_rt_found = False ; export_rt_values = ''
                    import_rt_found = False ; import_rt_values = ''
                    continue

            #     Table Id                   : 10
            #     Table Id                   : 0x80000001
            m = p26.match(line)
            if m:
                table_id = str(m.groupdict()['table_id'])
                if '0x' in table_id:
                    parsed_dict['vrf'][vrf_name]['address_family']\
                        [address_family]['table_id'] = table_id
                else:
                    parsed_dict['vrf'][vrf_name]['address_family']\
                        [address_family]['table_id'] = '0x' + table_id
                continue
            
            #     Table state                : UP
            m = p27.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['address_family'][address_family]\
                    ['table_state'] = str(m.groupdict()['table_state']).lower()
                continue

            #     Peers      Active-peers    Routes     Paths      Networks   Aggregates
            #     1          0               5          5          1          2      
            m = p28.match(line)
            if m:
                if 'peers' not in parsed_dict['vrf'][vrf_name]\
                    ['address_family'][address_family]:
                    parsed_dict['vrf'][vrf_name]['address_family']\
                        [address_family]['peers'] = {}

                peers = int(m.groupdict()['peers'])

                if peers not in parsed_dict['vrf'][vrf_name]['address_family']\
                    [address_family]['peers']:
                    parsed_dict['vrf'][vrf_name]['address_family']\
                        [address_family]['peers'][peers] = {}
                    parsed_dict['vrf'][vrf_name]['address_family']\
                        [address_family]['peers'][peers]['active_peers'] = \
                            int(m.groupdict()['active_peers'])
                    parsed_dict['vrf'][vrf_name]['address_family']\
                        [address_family]['peers'][peers]['routes'] = \
                            int(m.groupdict()['routes'])
                    parsed_dict['vrf'][vrf_name]['address_family']\
                        [address_family]['peers'][peers]['paths'] = \
                            int(m.groupdict()['paths'])
                    parsed_dict['vrf'][vrf_name]['address_family']\
                        [address_family]['peers'][peers]['networks'] = \
                            int(m.groupdict()['networks'])
                    parsed_dict['vrf'][vrf_name]['address_family']\
                        [address_family]['peers'][peers]['aggregates'] = \
                            int(m.groupdict()['aggregates'])
                    continue

            #     Redistribution                
            #         direct, route-map genie_redistribution
            #         static, route-map genie_redistribution
            #         eigrp, route-map test-map
            m = p29.match(line)
            if m:
                if 'redistribution' not in parsed_dict['vrf'][vrf_name]\
                    ['address_family'][address_family]:
                    parsed_dict['vrf'][vrf_name]['address_family']\
                        [address_family]['redistribution'] = {}

                name = str(m.groupdict()['name']).lower()

                if name not in parsed_dict['vrf'][vrf_name]['address_family']\
                    [address_family]['redistribution']:
                    parsed_dict['vrf'][vrf_name]['address_family']\
                        [address_family]['redistribution'][name] = {}
                    parsed_dict['vrf'][vrf_name]['address_family']\
                        [address_family]['redistribution'][name]\
                            ['route_map'] = str(m.groupdict()['route_map'])
                    continue
            
            # Export RT list:
            # Import RT list:
            # EVPN Export RT list:
            # EVPN Import RT list:
            # MVPN Export RT list:
            # MVPN Import RT list:
            # Export RT list: 100:1
            # Import RT list: 100:1
            m = p30.match(line)
            if m:
                rt_list_type = str(m.groupdict()['type']).lower()
                rt_list_type = rt_list_type.replace(' ', '_')
                rt_list_type += '_rt_list'
                values = ''
                if m.groupdict()['rt_list']:
                    values = values + ' ' + m.groupdict()['rt_list']
                    parsed_dict['vrf'][vrf_name]['address_family']\
                        [address_family][rt_list_type] = values.strip()
                continue

            # 100:1
            # 400:400
            # ASnumber:100 ASnumber:91100
            # ASnumber:91100
            m = p31.match(line)
            if m:
                values = values + ' ' + m.groupdict()['rt_list']
                parsed_dict['vrf'][vrf_name]['address_family'][address_family]\
                    [rt_list_type] = values.strip()
                continue

            #     Label mode: per-prefix
            m = p32.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['address_family'][address_family]\
                    ['label_mode'] = str(m.groupdict()['label_mode'])
                continue

            #     Is a Route-reflector
            m = p32_1.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['address_family'][address_family]\
                    ['route_reflector'] = True
                continue

            #     Aggregate label: 492287
            m = p33.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['address_family'][address_family]\
                    ['aggregate_label'] = str(m.groupdict()['aggregate_label'])
                continue

            #     Allocate-index:
            m = p33_1.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['address_family'][address_family] \
                    ['allocate_index'] = str(m.groupdict()['allocate_index'])
                continue

            # Import default limit       : 1000
            m = p34.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['address_family'][address_family]\
                    ['import_default_prefix_limit'] = \
                        int(m.groupdict()['import_default_prefix_limit'])
                continue

            # Import default prefix count : 3
            m = p35.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['address_family'][address_family]\
                    ['import_default_prefix_count'] = \
                        int(m.groupdict()['import_default_prefix_count'])

            # Import default map         : PERMIT_ALL_RM
            m = p36.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['address_family'][address_family]\
                    ['import_default_map'] = \
                        str(m.groupdict()['import_default_map'])

            # Export default limit       : 1000
            m = p37.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['address_family'][address_family]\
                    ['export_default_prefix_limit'] = \
                        int(m.groupdict()['export_default_prefix_limit'])

            # Export default prefix count : 2
            m = p38.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['address_family'][address_family]\
                    ['export_default_prefix_count'] = \
                        int(m.groupdict()['export_default_prefix_count'])

            # Export default map         : PERMIT_ALL_RM
            m = p39.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['address_family'][address_family]\
                    ['export_default_map'] = \
                        str(m.groupdict()['export_default_map'])

            # Nexthop trigger-delay
            m = p40.match(line)
            if m:
                if 'next_hop_trigger_delay' not in parsed_dict['vrf'][vrf_name]\
                    ['address_family'][address_family]:
                    parsed_dict['vrf'][vrf_name]['address_family']\
                        [address_family]['next_hop_trigger_delay'] = {}

            # critical 3000 ms
            m = p41.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['address_family']\
                    [address_family]['next_hop_trigger_delay']['critical'] = \
                    int(m.groupdict()['critical'])

            # non-critical 3000 ms
            m = p42.match(line)
            if m:
                parsed_dict['vrf'][vrf_name]['address_family']\
                    [address_family]['next_hop_trigger_delay']['non_critical'] = \
                        int(m.groupdict()['non_critical'])

        return parsed_dict

    def xml(self, vrf='', output=None):
        if output is None:
            if vrf:
                out = self.device.execute(self.xml_command[1].format(vrf=vrf))
            else:
                out = self.device.execute(self.xml_command[0])
        else:
            out = output

        etree_dict = {}
        # Remove junk characters returned by the device
        out = out.replace("]]>]]>", "")
        xml_output = ET.fromstring(out)

        for item in xml_output:
            for data in item:
                for show in data:
                    for bgp in show:
                        for __XML__OPT_Cmd_show_ip_bgp_session_cmd_vrf in bgp:
                            for process in __XML__OPT_Cmd_show_ip_bgp_session_cmd_vrf:
                                for __XML__OPT_Cmd_show_bgp_process_cmd_vrf in process:
                                    for __XML__OPT_Cmd_show_bgp_process_cmd___readonly__ in __XML__OPT_Cmd_show_bgp_process_cmd_vrf:
                                        for key in __XML__OPT_Cmd_show_bgp_process_cmd___readonly__:
                                            # Get key text
                                            text = key.tag[key.tag.find('}')+1:]
                                            # bgp_pid
                                            if text == 'processid':
                                                etree_dict['bgp_pid'] = int(key.text)
                                            # bgp_protocol_started_reason
                                            if text == 'protocolstartedreason':
                                                etree_dict['bgp_protocol_started_reason'] = key.text
                                            # bgp_tag
                                            if text == 'protocoltag':
                                                etree_dict['bgp_tag'] = key.text
                                            # bgp_protocol_state
                                            if text == 'protocolstate':
                                                etree_dict['bgp_protocol_state'] = str(key.text).lower()
                                            # bgp_isolate_mode
                                            if text == 'isolatemode':
                                                etree_dict['bgp_isolate_mode'] = key.text
                                            # bgp_mmode
                                            if text == 'mmode':
                                                etree_dict['bgp_mmode'] = key.text
                                            # bgp_memory_state
                                            if text == 'memorystate':
                                                etree_dict['bgp_memory_state'] = str(key.text).lower()
                                            # bgp_performance_mode
                                            if text == 'forwardingstatesaved':
                                                if key.text == 'false':
                                                    etree_dict['bgp_performance_mode'] = 'No'
                                                else:
                                                    etree_dict['bgp_performance_mode'] = 'Yes'
                                            # bgp_asformat
                                            if text == 'asformat':
                                                etree_dict['bgp_asformat'] = key.text
                                            if text == 'srgbmin':
                                                srgbin = key.text
                                            if text == 'srgbmax':
                                                srgmax = key.text
                                                try:
                                                    etree_dict['segment_routing_global_block'] = srgbin + '-' + srgmax
                                                except Exception:
                                                    pass
                                            # num_attr_entries
                                            if text == 'attributeentries':
                                                etree_dict['num_attr_entries'] = int(key.text)
                                            # hwm_attr_entries
                                            if text == 'hwmattributeentries':
                                                etree_dict['hwm_attr_entries'] = int(key.text)
                                            # bytes_used
                                            if text == 'bytesused':
                                                etree_dict['bytes_used'] = int(key.text)
                                            # entries_pending_delete
                                            if text == 'entriespendingdelete':
                                                etree_dict['entries_pending_delete'] = int(key.text)
                                            # hwm_entries_pending_delete
                                            if text == 'hwmentriespendingdelete':
                                                etree_dict['hwm_entries_pending_delete'] = int(key.text)
                                            # bgp_paths_per_hwm_attr
                                            if text == 'pathsperattribute':
                                                etree_dict['bgp_paths_per_hwm_attr'] = int(key.text)
                                            # bgp_as_path_entries
                                            if text == 'aspathentries':
                                                etree_dict['bgp_as_path_entries'] = int(key.text)
                                            # bytes_used_as_path_entries
                                            if text == 'aspathbytes':
                                                etree_dict['bytes_used_as_path_entries'] = int(key.text)
                                            
                                            if text == 'TABLE_vrf':
                                                for table_vrf in key:
                                                    for row_vrf in table_vrf:
                                                        vrf_tag = row_vrf.tag[row_vrf.tag.find('}')+1:]

                                                        # vrf
                                                        #   vrf_name
                                                        if vrf_tag == 'vrf-name-out':
                                                            vrf_name = row_vrf.text
                                                            if 'vrf' not in etree_dict:
                                                                etree_dict['vrf'] = {}
                                                            if vrf_name not in etree_dict['vrf']:
                                                                etree_dict['vrf'][vrf_name] = {}
                                                                vrf_dict = etree_dict['vrf'][vrf_name]
                                                        # vrf_id
                                                        if vrf_tag == 'vrf-id':
                                                            vrf_dict['vrf_id'] = row_vrf.text
                                                        # vrf_state
                                                        if vrf_tag == 'vrf-state':
                                                            vrf_dict['vrf_state'] = str(row_vrf.text).lower()
                                                        # router_id
                                                        if vrf_tag == 'vrf-router-id':
                                                            vrf_dict['router_id'] = row_vrf.text
                                                        # conf_router_id
                                                        if vrf_tag == 'vrf-cfgd-id':
                                                            vrf_dict['conf_router_id'] = row_vrf.text
                                                        # confed_id
                                                        if vrf_tag == 'vrf-confed-id':
                                                            vrf_dict['confed_id'] = int(row_vrf.text)
                                                        # cluster_id
                                                        if vrf_tag == 'vrf-cluster-id':
                                                           vrf_dict['cluster_id'] = row_vrf.text
                                                        # num_conf_peers
                                                        if vrf_tag == 'vrf-peers':
                                                            vrf_dict['num_conf_peers'] = int(row_vrf.text)
                                                        # num_pending_conf_peers
                                                        if vrf_tag == 'vrf-pending-peers':
                                                            vrf_dict['num_pending_conf_peers'] = int(row_vrf.text)
                                                        # num_established_peers
                                                        if vrf_tag == 'vrf-est-peers':
                                                            vrf_dict['num_established_peers'] = int(row_vrf.text)
                                                            vrf_dict['vrf_rd'] = 'not configured'
                                                        # vrf_rd
                                                        if vrf_tag == 'vrf-rd':
                                                            vrf_dict['vrf_rd'] = row_vrf.text

                                                        if vrf_tag == 'TABLE_af':
                                                            for table_af in row_vrf:
                                                                for row_af in table_af:
                                                                    af_tag = row_af.tag[row_af.tag.find('}')+1:]

                                                                    # address_family
                                                                    #   address_family_name
                                                                    if af_tag == 'af-name':
                                                                        address_family_name = str(row_af.text).lower()
                                                                        if 'address_family' not in etree_dict['vrf'][vrf_name]:
                                                                            etree_dict['vrf'][vrf_name]['address_family'] = {}
                                                                        if address_family_name not in etree_dict['vrf'][vrf_name]['address_family']:
                                                                            etree_dict['vrf'][vrf_name]['address_family'][address_family_name] = {}
                                                                            af_dict = etree_dict['vrf'][vrf_name]['address_family'][address_family_name]
                                                                        # Initialize empty lists
                                                                        export_rt_list = ''
                                                                        import_rt_list = ''
                                                                    # table_id
                                                                    if af_tag == 'af-table-id':
                                                                        table_id = str(row_af.text)
                                                                        if '0x' in table_id:
                                                                            af_dict['table_id'] = table_id
                                                                        else:
                                                                            af_dict['table_id'] = '0x' + table_id
                                                                    # table_state
                                                                    if af_tag == 'af-state':
                                                                        af_dict['table_state'] = str(row_af.text).lower()
                                                                    # peers
                                                                    if af_tag == 'af-num-peers':
                                                                        peers = int(row_af.text)
                                                                        if 'peers' not in af_dict:
                                                                            af_dict['peers'] = {}
                                                                        if peers not in af_dict['peers']:
                                                                            af_dict['peers'][peers] = {}
                                                                    # active_peers
                                                                    if af_tag == 'af-num-active-peers':
                                                                        af_dict['peers'][peers]['active_peers'] = int(row_af.text)
                                                                    # routes
                                                                    if af_tag == 'af-peer-routes':
                                                                        af_dict['peers'][peers]['routes'] = int(row_af.text)
                                                                    # paths
                                                                    if af_tag == 'af-peer-paths':
                                                                        af_dict['peers'][peers]['paths'] = int(row_af.text)
                                                                    # networks
                                                                    if af_tag == 'af-peer-networks':
                                                                        af_dict['peers'][peers]['networks'] = int(row_af.text)
                                                                    # aggregates
                                                                    if af_tag == 'af-peer-aggregates':
                                                                        af_dict['peers'][peers]['aggregates'] = int(row_af.text)
                                                                    # route_reflector
                                                                    if af_tag == 'af-rr':
                                                                        if row_af.text == 'true':
                                                                            af_dict['route_reflector'] = True
                                                                    # next_hop_trigger_delay
                                                                    #   critical
                                                                    if af_tag == 'nexthop-trigger-delay-critical':
                                                                        if 'next_hop_trigger_delay' not in af_dict:
                                                                            af_dict['next_hop_trigger_delay'] = {}
                                                                        af_dict['next_hop_trigger_delay']['critical'] = int(row_af.text)
                                                                    # next_hop_trigger_delay
                                                                    #   non_critical
                                                                    if af_tag == 'nexthop-trigger-delay-non-critical':
                                                                        af_dict['next_hop_trigger_delay']['non_critical'] = int(row_af.text)
                                                                    # aggregate_label
                                                                    if af_tag == 'af-aggregate-label':
                                                                        af_dict['aggregate_label'] = row_af.text
                                                                    # label_mode
                                                                    if af_tag == 'af-label-mode':
                                                                        af_dict['label_mode'] = row_af.text
                                                                    # import_default_map
                                                                    if af_tag == 'importdefault_map':
                                                                        af_dict['import_default_map'] = row_af.text
                                                                    # import_default_prefix_limit
                                                                    if af_tag == 'importdefault_prefixlimit':
                                                                        af_dict['import_default_prefix_limit'] = int(row_af.text)
                                                                    # import_default_prefix_count
                                                                    if af_tag == 'importdefault_prefixcount':
                                                                        af_dict['import_default_prefix_count'] = int(row_af.text)
                                                                    # export_default_map
                                                                    if af_tag == 'exportdefault_map':
                                                                        af_dict['export_default_map'] = row_af.text
                                                                    # export_default_prefix_limit
                                                                    if af_tag == 'exportdefault_prefixlimit':
                                                                        af_dict['export_default_prefix_limit'] = int(row_af.text)
                                                                    # export_default_prefix_count
                                                                    if af_tag == 'exportdefault_prefixcount':
                                                                        af_dict['export_default_prefix_count'] = int(row_af.text)

                                                                    # TABLE_redist
                                                                    #   ROW_redist
                                                                    if af_tag == 'TABLE_redist':
                                                                        for table_redist in row_af:
                                                                            for row_redist in table_redist:
                                                                                row_redist_tag = row_redist.tag[row_redist.tag.find('}')+1:]
                                                                                # protocol
                                                                                if row_redist_tag == 'protocol':
                                                                                    protocol = row_redist.text
                                                                                    if 'redistribution' not in af_dict:
                                                                                        af_dict['redistribution'] = {}
                                                                                    if protocol not in af_dict['redistribution']:
                                                                                        af_dict['redistribution'][protocol] = {}
                                                                                # route_map
                                                                                if row_redist_tag == 'route-map':
                                                                                    af_dict['redistribution'][protocol]['route_map'] = row_redist.text

                                                                    # TABLE_evpn_export_rt
                                                                    #   ROW_evpn_export_rt
                                                                    if af_tag == 'TABLE_evpn_export_rt':
                                                                        for table_evpn_export in row_af:
                                                                            for row_export in table_evpn_export:
                                                                                row_export_tag = row_export.tag[row_export.tag.find('}')+1:]
                                                                                # export_rt_list
                                                                                if row_export_tag == 'evpn-export-rt':
                                                                                    export_rt_list = str(export_rt_list + ' ' + row_export.text).strip()
                                                                                    af_dict['export_rt_list'] = export_rt_list
                                                                    # TABLE_evpn_import_rt
                                                                    #   ROW_evpn_import_rt
                                                                    if af_tag == 'TABLE_evpn_import_rt':
                                                                        for table_evpn_import in row_af:
                                                                            for row_import in table_evpn_import:
                                                                                row_import_tag = row_import.tag[row_import.tag.find('}')+1:]
                                                                                # export_rt_list
                                                                                if row_import_tag == 'evpn-import-rt':
                                                                                    import_rt_list = str(import_rt_list + ' ' + row_import.text).strip()
                                                                                    af_dict['import_rt_list'] = import_rt_list

                                                                    # parsed all tags
                                                                    continue
                                                                                    
        return etree_dict

    def yang(self, vrf=''):
        # Initialize empty dictionary
        map_dict = {}

        # Execute YANG 'get' operational state RPC and parse the XML
        bgpOC = BgpOpenconfigYang(self.device)
        yang_dict = bgpOC.yang()

        # Map keys from yang_dict to map_dict

        # bgp_pid
        map_dict['bgp_pid'] = yang_dict['bgp_pid']

        # vrf

        for vrf_name in yang_dict['vrf']:
            if 'vrf' not in map_dict:
                map_dict['vrf'] = {}
            if vrf_name not in map_dict['vrf']:
                map_dict['vrf'][vrf_name] = {}
            for vrf_attr_key in yang_dict['vrf'][vrf_name]:
                # Set router_id
                if vrf_attr_key == 'router_id':
                    map_dict['vrf'][vrf_name][vrf_attr_key] = yang_dict['vrf'][vrf_name][vrf_attr_key]
                # Set address_family
                if vrf_attr_key == 'address_family':
                    map_dict['vrf'][vrf_name][vrf_attr_key] = yang_dict['vrf'][vrf_name][vrf_attr_key]
                if vrf_attr_key == 'neighbor':
                    for nbr in yang_dict['vrf'][vrf_name]['neighbor']:
                        for key in yang_dict['vrf'][vrf_name]['neighbor'][nbr]:
                            # Set cluster_id
                            if key == 'route_reflector_cluster_id':
                                cluster_id = '0.0.0' + str(yang_dict['vrf'][vrf_name]['neighbor'][nbr]['route_reflector_cluster_id'])
                                map_dict['vrf'][vrf_name]['cluster_id'] = cluster_id

        # Return to caller
        return map_dict


# =========================================
# Schema for 'show bgp peer-session <WORD>'
# =========================================
class ShowBgpPeerSessionSchema(MetaParser):
    """Schema for show bgp peer-session <peer_session>"""

    schema = {
        'peer_session': 
            {Any(): 
                {Optional('shutdown'): bool,
                 Optional('update_source'): str,
                 Optional('description'): str,
                 Optional('password'): bool,
                 Optional('ebgp_multihop_enable'): bool,
                 Optional('ebgp_multihop_limit'): int,
                 Optional('disable_connectivity_check'): bool,
                 Optional('suppress_capabilities'): bool,
                 Optional('transport_connection_mode'): str,
                 Optional('holdtime'): int,
                 Optional('keepalive'): int,
                 Optional('remote_as'): bool,
                 Optional('local_as'): bool,
                 Optional('bfd'): bool,
                 Optional('inherited_vrf_default'): str,
                },
            },
        }

# =========================================
# Parser for 'show bgp peer-session <WORD>'
# =========================================
class ShowBgpPeerSession(ShowBgpPeerSessionSchema):

    """Parser for:
        show bgp peer-session <peer_session>
        Executing 'show running-config bgp | inc peer-session' to collect
        configured peer-session names.
    """
    cli_command = 'show running-config | inc peer-session'

    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        # Init vars
        peer_sessions = []
        parsed_dict = {}

        p1 = re.compile(r'^\s*template +peer-session '
                    r'+(?P<session_name>[a-zA-Z\-\_0-9]+)$')
        r1 = re.compile(r'^\s*Shutdown$')
        r2 = re.compile(r'^\s*Update +Source +-'
                    r' +(?P<update_source>[a-zA-Z0-9\:\s]+)$')
        r3 = re.compile(r'^\s*Description +- +description *:'
                    r' +(?P<desc>[a-zA-Z\-]+)$')
        r4 = re.compile(r'^\s*Password$')
        r5 = re.compile(r'^\s*EBGP +Multihop +- +hop +limit *:'
                    r' +(?P<ebgp_multihop_limit>[0-9]+)$')
        r6 = re.compile(r'^\s*Disable +Connectivity +Check$')
        r7 = re.compile(r'^\s*Suppress +Capabilities$')
        r8 = re.compile(r'^\s*Passive Only$')
        r9 = re.compile(r'^\s*Timers +- +hold +time *:'
                    r' +(?P<holdtime>[0-9]+), keepalive *:'
                    r' +(?P<keepalive>[0-9]+)$')
        r10 = re.compile(r'^\s*Remote AS$')
        r11 = re.compile(r'^\s*Local AS$')
        r12 = re.compile(r'^\s*Enable Bfd$')
        r13 = re.compile(r'^\s*VRF +default *:'
                    r' +(?P<vrf_default>[0-9\.]+)$')

        for line in out.splitlines():
            line = line.rstrip()

            # template peer-session PEER-SESSION
            # template peer-session PS-1
            m = p1.match(line)
            if m:
                # Create top level key
                if 'peer_session' not in parsed_dict:
                    parsed_dict['peer_session'] = {}
                # Get session name and save it for later
                peer_sessions.append(str(m.groupdict()['session_name']))
                continue

        if peer_sessions:
            
            # Execute bgp show command now
            for session in peer_sessions:
                # Create session key
                if session not in parsed_dict['peer_session']:
                    parsed_dict['peer_session'][session] = {}
                    sub_dict = parsed_dict['peer_session'][session]
                
                base_cmd = 'show bgp peer-session ' + session
                cmd = base_cmd
                out = self.device.execute(cmd)

                for line in out.splitlines():
                    line = line.rstrip()

                    # Commands configured in this template:
                    # Shutdown
                    m = r1.match(line)
                    if m:
                        sub_dict['shutdown'] = True
                        continue
                  
                    # Update Source - interface: loopback0
                    m = r2.match(line)
                    if m:
                        sub_dict['update_source'] = \
                            str(m.groupdict()['update_source']).lower()
                        continue
                  
                    # Description - description: PEER-SESSION
                    m = r3.match(line)
                    if m:
                        sub_dict['description'] = \
                            str(m.groupdict()['desc'])
                        continue
                  
                    # Password
                    m = r4.match(line)
                    if m:
                        sub_dict['password'] = True
                        continue
                  
                    # EBGP Multihop - hop limit: 255
                    m = r5.match(line)
                    if m:
                        sub_dict['ebgp_multihop_enable'] = True
                        sub_dict['ebgp_multihop_limit'] = \
                            int(m.groupdict()['ebgp_multihop_limit'])
                        continue
                  
                    # Disable Connectivity Check
                    m = r6.match(line)
                    if m:
                        sub_dict['disable_connectivity_check'] = True
                        continue
                    
                    # Suppress Capabilities
                    m = r7.match(line)
                    if m:
                        sub_dict['suppress_capabilities'] = True
                        continue
                  
                    # Passive Only
                    m = r8.match(line)
                    if m:
                        sub_dict['transport_connection_mode'] = 'Passive'
                        continue
                  
                    # Timers - hold time: 111, keepalive: 222
                    m = r9.match(line)
                    if m:
                        sub_dict['holdtime'] = int(m.groupdict()['holdtime'])
                        sub_dict['keepalive'] = int(m.groupdict()['keepalive'])
                        continue
                    
                    # Remote AS
                    m = r10.match(line)
                    if m:
                        sub_dict['remote_as'] = True
                        continue
                  
                    # Local AS
                    m = r11.match(line)
                    if m:
                        sub_dict['local_as'] = True
                        continue
                  
                    # Enable Bfd
                    m = r12.match(line)
                    if m:
                        sub_dict['bfd'] = True
                        continue
                
                    # Inherited commands:
                    # Inherited by the following peers:
                    # VRF default: 10.16.2.5
                    m = r13.match(line)
                    if m:
                        sub_dict['inherited_vrf_default'] = \
                            str(m.groupdict()['vrf_default'])
                        continue

        # Return parsed output
        return parsed_dict


# ========================================
# Schema for 'show bgp peer-policy <WORD>'
# ========================================
class ShowBgpPeerPolicySchema(MetaParser):
    """Schema for show bgp peer-policy <peer_policy>"""

    schema = {
        'peer_policy': 
            {Any(): 
                {Optional('send_community'): bool,
                 Optional('send_ext_community'): bool,
                 Optional('route_reflector_client'): bool,
                 Optional('route_map_name_in'): str,
                 Optional('route_map_name_out'): str,
                 Optional('maximum_prefix_max_prefix_no'): int,
                 Optional('default_originate'): bool,
                 Optional('default_originate_route_map'): str,
                 Optional('soft_reconfiguration'): bool,
                 Optional('site_of_origin'): bool,
                 Optional('allowas_in'): bool,
                 Optional('as_override'): bool,
                 Optional('inherited_vrf_default'): str,
                 Optional('next_hop_self'): bool,
                },
            },
        }

# ========================================
# Parser for 'show bgp peer-policy <WORD>'
# ========================================
class ShowBgpPeerPolicy(ShowBgpPeerPolicySchema):
    """Parser for:
        show bgp peer-policy <peer_policy>
        Executing 'show running-config bgp | inc peer-policy' to collect
        configured peer-policy names.
    """
    cli_command = 'show running-config | inc peer-policy'

    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output
        
        # Init vars
        policy_names = []
        parsed_dict = {}

        p1 = re.compile(r'^\s*template +peer-policy'
                    r' +(?P<policy_name>[a-zA-Z0-9\-\_]+)$')
        r1 = re.compile(r'^\s*Send +Community$')
        r2 = re.compile(r'^\s*Send +Ext-community$')
        r3 = re.compile(r'^\s*Route +Reflector +Client$')
        r4 = re.compile(r'^\s*Route-map +Inbound +- +policy-name *:'
                            r' +(?P<inbound_name>[a-zA-Z\-]+)$')
        r5 = re.compile(r'^\s*Route-map +Outbound +- +policy-name *:'
                            r' +(?P<outbound_name>[a-zA-Z\-]+)$')
        r6 = re.compile(r'^\s*Maximum +Prefixes +- +prefix +limit *:'
                            r' +(?P<max_prefix_no>[0-9]+)$')
        r7 = re.compile(r'^\s*Default +Originate(?: +- +route-map *:'
                            r' +(?P<route_map>[a-zA-Z]+))?$')
        r8 = re.compile(r'^\s*Soft-Reconfig$')
        r9 = re.compile(r'^\s*Site-of-origin$')
        r10 = re.compile(r'^\s*Allowas-in$')
        r11 = re.compile(r'^\s*AS-override$')
        r12 = re.compile(r'^\s*VRF +default *:'
                            r' +(?P<vrf_default>[0-9\.]+)$')
        r13 = re.compile(r'^\s*Nexthop +Self$')

        for line in out.splitlines():
            line = line.rstrip()

            # template peer-policy PEER-POLICY
            m = p1.match(line)
            if m:
                # Get session name and save it for later
                policy_names.append(str(m.groupdict()['policy_name']))
                
                # Create top level key
                if 'peer_policy' not in parsed_dict:
                    parsed_dict['peer_policy'] = {}
                
                continue

        if policy_names:
            
            # Execute bgp show command now
            for policy_name in policy_names:
                
                # Create policy_name key
                if policy_name not in parsed_dict['peer_policy']:
                    parsed_dict['peer_policy'][policy_name] = {}
                    sub_dict = parsed_dict['peer_policy'][policy_name]
                
                base_cmd = 'show bgp peer-policy ' + policy_name
                cmd = base_cmd
                out = self.device.execute(cmd)

                for line in out.splitlines():
                    line = line.rstrip()

                    # Commands configured in this template:
                    # Send Community
                    m = r1.match(line)
                    if m:
                        sub_dict['send_community'] = True
                        continue
                  
                    # Send Ext-community
                    m = r2.match(line)
                    if m:
                        sub_dict['send_ext_community'] = True
                        continue
                  
                    # Route Reflector Client
                    m = r3.match(line)
                    if m:
                        sub_dict['route_reflector_client'] = True
                        continue
                  
                    # Route-map Inbound - policy-name: test-map
                    m = r4.match(line)
                    if m:
                        sub_dict['route_map_name_in'] = \
                            str(m.groupdict()['inbound_name'])
                        continue
                  
                    # Route-map Outbound - policy-name: test-map
                    m = r5.match(line)
                    if m:
                        sub_dict['route_map_name_out'] = \
                            str(m.groupdict()['outbound_name'])
                  
                    # Maximum Prefixes - prefix limit: 300
                    m = r6.match(line)
                    if m:
                        sub_dict['maximum_prefix_max_prefix_no'] = \
                            int(m.groupdict()['max_prefix_no'])
                        continue
                    
                    # Default Originate - route-map: test
                    m = r7.match(line)
                    if m:
                        sub_dict['default_originate'] =  True
                        sub_dict['default_originate_route_map'] = \
                            str(m.groupdict()['route_map'])
                        continue
                  
                    # Soft-Reconfig
                    m = r8.match(line)
                    if m:
                        sub_dict['soft_reconfiguration'] = True
                        continue
                  
                    # Site-of-origin
                    m = r9.match(line)
                    if m:
                        sub_dict['site_of_origin'] = True
                        continue
                    
                    # Allowas-in
                    m = r10.match(line)
                    if m:
                        sub_dict['allowas_in'] = True
                        continue
                  
                    # AS-override
                    m = r11.match(line)
                    if m:
                        sub_dict['as_override'] = True
                        continue
                
                    # Inherited commands:
                    # Inherited by the following peers:
                    # VRF default: 10.16.2.5
                    m = r12.match(line)
                    if m:
                        sub_dict['inherited_vrf_default'] = \
                            str(m.groupdict()['vrf_default'])
                        continue

                    # Nexthop Self
                    m = r13.match(line)
                    if m:
                        sub_dict['next_hop_self'] = True
                        continue

        # Return parsed output
        return parsed_dict


# ===================================================
# Schema for 'show bgp peer-template <peer_template>'
# ===================================================
class ShowBgpPeerTemplateSchema(MetaParser):
    """Schema for show bgp peer-template <peer_template>"""

    schema = {
        'peer_template':
            {Any():
                {Optional('remote_as'): int,
                Optional('inherit_template'): str,
                Optional('description'): str,
                Optional('update_source'): str,
                Optional('disable_connected_check'): bool,
                Optional('bfd_live_detection'): bool,
                Optional('num_hops_bgp_peer'): int,
                Optional('tcp_md5_auth'): str,
                Optional('nbr_transport_connection_mode'): str,
                Optional('nbr_local_as_cmd'): str,
                Optional('private_as_updates'): bool,
                Optional('holdtime'): int,
                Optional('keepalive_interval'): int,
                },
            },
        }

# ===================================================
# Parser for 'show bgp peer-template <peer_template>'
# ===================================================
class ShowBgpPeerTemplate(ShowBgpPeerTemplateSchema):

    '''Parser for show bgp peer-template <peer_template>
       Executing 'show running-config bgp | inc peer' to colllect
       configured peer-template names.
    '''
    cli_command = 'show running-config | inc peer'

    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        p0 = re.compile(r'^\s*template +peer'
                        r' +(?P<peer_template>[a-zA-Z0-9\-\_]+)$')
        p1 = re.compile(r'^\s*Remote +AS +(?P<remote_as>[0-9]+)$')
        p2 = re.compile(r'^\s*Inherits +session +configuration'
                            r' +from session-template'
                            r' +(?P<inherit_template>(\S+))$')
        p3 = re.compile(r'^\s*Description *: +(?P<desc>(\S+))$')
        p4 = re.compile(r'^\s*Using +(?P<update_source>(\S+)) +as'
                            r' +update +source +for +this +peer$')
        p5 = re.compile(r'^\s*Connected check is disabled$')
        p6 = re.compile(r'^\s*BFD live-detection +is +configured$')
        p7 = re.compile(r'^\s*External +BGP +peer +might +be +upto'
                            r' +(?P<num_hops_bgp_peer>[0-9]+) +hops'
                            r' +away$')
        p8 = re.compile(r'^\s*TCP +MD5 +authentication +is'
                            r' +(?P<tcp_md5_auth>(\S+))$')
        p9 = re.compile(r'^\s*Only +passive +connection +setup'
                            r' +allowed$')
        p10 = re.compile(r'^\s*Neighbor +local-as +command'
                            r' +(?P<nbr_local_as_cmd>(\S+))$')
        p11 = re.compile(r'^\s*Private +AS +numbers +removed +from'
                            r' +updates +sent +to +this +neighbor$')
        p12 = re.compile(r'^\s*Hold +time += +(?P<holdtime>[0-9]+),'
                            r' +keepalive +interval +is'
                            r' +(?P<keepalive_interval>[0-9]+)'
                            r' +seconds$')
                                    
        # Init vars
        peer_templates = []
        parsed_dict = {}

        for line in out.splitlines():
            line = line.rstrip()

            # template peer PEER
            m = p0.match(line)
            if m:
                # Get session name and save it for later
                peer_templates.append(str(m.groupdict()['peer_template']))
                
                # Create top level key
                if 'peer_template' not in parsed_dict:
                    parsed_dict['peer_template'] = {}
                continue

        if peer_templates:
            
            # Execute bgp show command now
            for peer_template in peer_templates:
                
                # Create template_names key
                if peer_template not in parsed_dict['peer_template']:
                    parsed_dict['peer_template'][peer_template] = {}
                    sub_dict = parsed_dict['peer_template'][peer_template]
                
                base_cmd = 'show bgp peer-template ' + peer_template
                cmd = base_cmd
                out = self.device.execute(cmd)

                for line in out.splitlines():
                    line = line.rstrip()

                    # BGP peer-template is PEER
                    # Remote AS 500
                    m = p1.match(line)
                    if m:
                        sub_dict['remote_as'] = int(m.groupdict()['remote_as'])
                        continue

                    # Inherits session configuration from session-template PEER-SESSION
                    m = p2.match(line)
                    if m:
                        sub_dict['inherit_template'] = \
                            str(m.groupdict()['inherit_template'])
                        continue

                    # Description: DESC
                    m = p3.match(line)
                    if m:
                        sub_dict['description'] = str(m.groupdict()['desc'])
                        continue

                    # Using loopback1 as update source for this peer
                    m = p4.match(line)
                    if m:
                        sub_dict['update_source'] = \
                            str(m.groupdict()['update_source'])
                        continue

                    # Connected check is disabled
                    m = p5.match(line)
                    if m:
                        sub_dict['disable_connected_check'] = True
                        continue

                    # BFD live-detection is configured
                    m = p6.match(line)
                    if m:
                        sub_dict['bfd_live_detection'] = True
                        continue

                    # External BGP peer might be upto 255 hops away
                    m = p7.match(line)
                    if m:
                        sub_dict['num_hops_bgp_peer'] = \
                            int(m.groupdict()['num_hops_bgp_peer'])
                        continue

                    # TCP MD5 authentication is enabled
                    m = p8.match(line)
                    if m:
                        sub_dict['tcp_md5_auth'] = \
                            str(m.groupdict()['tcp_md5_auth'])
                        continue

                    # Only passive connection setup allowed
                    m = p9.match(line)
                    if m:
                        sub_dict['nbr_transport_connection_mode'] = 'Passive'
                        continue

                    # Neighbor local-as command not active
                    m = p10.match(line)
                    if m:
                        sub_dict['nbr_local_as_cmd'] = \
                            str(m.groupdict()['nbr_local_as_cmd'])
                        continue

                    # Private AS numbers removed from updates sent to this neighbor
                    m = p11.match(line)
                    if m:
                        sub_dict['private_as_updates'] = False
                        continue

                    # Hold time = 26, keepalive interval is 13 seconds
                    m = p12.match(line)
                    if m:
                        sub_dict['holdtime'] = \
                            int(m.groupdict()['holdtime'])
                        sub_dict['keepalive_interval'] = \
                            int(m.groupdict()['keepalive_interval'])
                        continue


        # Return parsed output
        return parsed_dict




# ======================================================================
# Parser for 'show bgp l2vpn evpn neighbors <neighbor> advertised-routes
# ======================================================================
class ShowBgpL2vpnEvpnNeighborsAdvertisedRoutes(ShowBgpVrfAllNeighborsAdvertisedRoutes):
    """Parser for show bgp l2vpn evpn neighbors <neighbor> advertised-routes"""
    cli_command = 'show bgp l2vpn evpn neighbors {neighbor} advertised-routes'

    def cli(self, neighbor, output=None):
        if output is None:
            out = self.device.execute(self.cli_command.format(neighbor=neighbor))
        else:
            out = output

        return super().cli(neighbor=neighbor, output=out)



# ====================================
# Schema for 'show running-config bgp'
# ====================================
class ShowRunningConfigBgpSchema(MetaParser):
    """Schema for show running-config bgp"""

    schema = {
        'bgp':
            {'instance':
                {'default':
                    {
                    'bgp_id': int,
                    'protocol_shutdown': bool,
                    Optional('ps_name'):
                        {Any():
                            {'ps_fall_over_bfd': bool,
                            'ps_suppress_four_byte_as_capability': bool,
                            Optional('ps_description'): str,
                            'ps_disable_connected_check': bool,
                            'ps_ebgp_multihop': bool,
                            Optional('ps_ebgp_multihop_max_hop'): int,
                            Optional('ps_local_as_as_no'): int,
                            'ps_local_as_no_prepend': bool,
                            'ps_local_as_dual_as': bool,
                            'ps_local_as_replace_as': bool,
                            Optional('ps_password_text'): str,
                            Optional('ps_remote_as'): int,
                            'ps_shutdown': bool,
                            Optional('ps_keepalive_interval'): int,
                            Optional('ps_hodltime'): int,
                            Optional('ps_transport_connection_mode'): str,
                            Optional('ps_update_source'): str}},
                    Optional('pp_name'):
                        {Any():
                            {Optional('pp_allowas_in'): bool,
                             Optional('pp_allowas_in_as_number'): int,
                             Optional('pp_as_override'): bool,
                             Optional('pp_default_originate'): bool,
                             Optional('pp_default_originate_route_map'): str,
                             Optional('pp_route_map_name_in'): str,
                             Optional('pp_route_map_name_out'): str,
                             Optional('pp_maximum_prefix_max_prefix_no'): int,
                             Optional('pp_maximum_prefix_threshold'): int,
                             Optional('pp_maximum_prefix_restart'): int,
                             Optional('pp_maximum_prefix_warning_only'): bool,
                             Optional('pp_next_hop_self'): bool,
                             Optional('pp_route_reflector_client'): bool,
                             Optional('pp_send_community'): str,
                             'pp_soft_reconfiguration': bool,
                             Optional('pp_soo'): str,
                             }},
                    Optional('peer_name'):
                        {Any():
                             {Optional('peer_fall_over_bfd'): bool,
                              Optional('peer_remote_as'): int,
                              Optional('peer_password_text'): str,
                              Optional('peer_af_name'): {
                                  Any(): {
                                      Optional('peer_af_send_community'): str,
                                      Optional('peer_maximum_prefix_max_prefix_no'): int,
                                      Optional('peer_maximum_prefix_threshold'): int,
                                      Optional('peer_maximum_prefix_warning_only'): bool,
                                      Optional('peer_next_hop_self'): bool,
                                    }
                                 },
                              },
                        },
                    'vrf':
                        {Any():
                            {
                            Optional('rd'): str,
                            Optional('always_compare_med'): bool,
                            Optional('bestpath_compare_routerid'): bool,
                            Optional('bestpath_cost_community_ignore'): bool,
                            Optional('bestpath_med_missing_at_worst'): bool,
                            Optional('cluster_id'): str,
                            Optional('confederation_identifier'): int,
                            Optional('confederation_peers_as'): str,
                            'graceful_restart': bool,
                            Optional('graceful_restart_restart_time'): int,
                            Optional('graceful_restart_stalepath_time'): int,
                            'log_neighbor_changes': bool,
                            Optional('router_id'): str,
                            Optional('keepalive_interval'): int,
                            Optional('holdtime'): int,
                            'enforce_first_as': bool,
                            'fast_external_fallover': bool,
                            Optional('default_choice_ipv4_unicast'): str,
                            Optional('dynamic_med_interval'): int,
                            Optional('shutdown'): str,
                            'flush_routes': bool,
                            'isolate': bool,
                            Optional('disable_policy_batching_ipv4'): str,
                            Optional('disable_policy_batching_ipv6'): str,
                            Optional('af_name'):
                                {Any():
                                    {
                                    Optional('af_evpn_vni_rt_type'): str,
                                    Optional('af_evpn_vni_rt'): str,
                                    Optional('af_dampening'): bool,
                                    Optional('af_dampening_route_map'): str,
                                    Optional('af_dampening_half_life_time'): int,
                                    Optional('af_dampening_reuse_time'): int,
                                    Optional('af_dampening_suppress_time'): int,
                                    Optional('af_dampening_max_suppress_time'): int,
                                    Optional('af_default_originate'): bool,
                                    Optional('af_nexthop_route_map'): str,
                                    Optional('af_nexthop_trigger_enable'): bool,
                                    Optional('af_nexthop_trigger_delay_critical'): int,
                                    Optional('af_nexthop_trigger_delay_non_critical'): int,
                                    Optional('af_client_to_client_reflection'): bool,
                                    Optional('af_distance_extern_as'): int,
                                    Optional('af_distance_internal_as'): int,
                                    Optional('af_distance_local'): int,
                                    Optional('af_maximum_paths_ebgp'): int,
                                    Optional('af_maximum_paths_ibgp'): int,
                                    Optional('af_maximum_paths_eibgp'): int,
                                    Optional('af_additional_paths_send'): bool,
                                    Optional('af_additional_paths_receive'): bool,
                                    Optional('af_aggregate_address_ipv4_address'): str,
                                    Optional('af_aggregate_address_ipv4_mask'): int,
                                    Optional('af_aggregate_address_as_set'): bool,
                                    Optional('af_aggregate_address_summary_only'): bool,
                                    Optional('af_network_number'): Or(str, ListOf(str)),
                                    Optional('af_network_mask'): Or(int, ListOf(int)),
                                    Optional('af_network_route_map'): str,
                                    Optional('af_redist_isis'): str,
                                    Optional('af_redist_isis_metric'): str,
                                    Optional('af_redist_isis_route_policy'): str,
                                    Optional('af_redist_ospf'): str,
                                    Optional('af_redist_ospf_metric'): str,
                                    Optional('af_redist_ospf_route_policy'): str,
                                    Optional('af_redist_rip'): str,
                                    Optional('af_redist_rip_metric'): str,
                                    Optional('af_redist_rip_route_policy'): str,
                                    Optional('af_redist_static'): bool,
                                    Optional('af_redist_static_metric'): str,
                                    Optional('af_redist_static_route_policy'): str,
                                    Optional('af_redist_connected'): bool,
                                    Optional('af_redist_connected_metric'): str,
                                    Optional('af_redist_connected_route_policy'): str,
                                    Optional('af_v6_aggregate_address_ipv6_address'): str,
                                    Optional('af_v6_aggregate_address_as_set'): bool,
                                    Optional('af_v6_aggregate_address_summary_only'): bool,
                                    Optional('af_v6_network_number'): str,
                                    Optional('af_v6_network_route_map'): str,
                                    Optional('af_v6_allocate_label_all'): bool,
                                    Optional('af_retain_rt_all'): bool,
                                    Optional('af_label_allocation_mode'): str,
                                    Optional('af_advertise_pip'): bool
                                     }
                                 },
                            Optional('neighbor_id'):
                                {Any():
                                    {Optional('nbr_fall_over_bfd'): bool,
                                     Optional('nbr_suppress_four_byte_as_capability'): bool,
                                     Optional('nbr_description'): str,
                                     Optional('nbr_disable_connected_check'): bool,
                                     Optional('nbr_ebgp_multihop'): bool,
                                     Optional('nbr_ebgp_multihop_max_hop'): int,
                                     Optional('nbr_inherit_peer_session'): str,
                                     Optional('nbr_local_as_as_no'): int,
                                     Optional('nbr_local_as_no_prepend'): bool,
                                     Optional('nbr_local_as_replace_as'): bool,
                                     Optional('nbr_local_as_dual_as'): bool,
                                     Optional('nbr_remote_as'): int,
                                     Optional('nbr_remove_private_as'): bool,
                                     Optional('nbr_shutdown'): bool,
                                     Optional('nbr_keepalive_interval'): int,
                                     Optional('nbr_holdtime'): int,
                                     Optional('nbr_update_source'): str,
                                     Optional('nbr_password_text'): str,
                                     Optional('nbr_transport_connection_mode'): str,
                                     Optional('nbr_peer_type'): str,
                                     Optional('nbr_inherit_peer'): str,
                                     Optional('nbr_af_name'):
                                        {Any():
                                            {Optional('nbr_af_allowas_in'): bool,
                                            Optional('nbr_af_allowas_in_as_number'): int,
                                            Optional('nbr_af_inherit_peer_policy'): str,
                                            Optional('nbr_af_inherit_peer_seq'): int,
                                            Optional('nbr_af_maximum_prefix_max_prefix_no'): int,
                                            Optional('nbr_af_maximum_prefix_threshold'): int,
                                            Optional('nbr_af_maximum_prefix_restart'): int,
                                            Optional('nbr_af_maximum_prefix_warning_only'): bool,
                                            Optional('nbr_af_route_map_name_in'): str,
                                            Optional('nbr_af_route_map_name_out'): str,
                                            Optional('no_nbr_af_route_map_name_in'): str,
                                            Optional('no_nbr_af_route_map_name_out'): str,
                                            Optional('nbr_af_route_reflector_client'): bool,
                                            Optional('nbr_af_send_community'): str,
                                            Optional('nbr_af_rewrite_evpn_rt_asn'): bool,
                                            Optional('nbr_af_soft_reconfiguration'): bool,
                                            Optional('nbr_af_next_hop_self'): bool,
                                            Optional('nbr_af_as_override'): bool,
                                            Optional('nbr_af_default_originate'): bool,
                                            Optional('nbr_af_default_originate_route_map'): str,
                                            Optional('nbr_af_soo'): str},
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
        Optional('vxlan'): {
            'evpn': {
                Optional('evpn_vni'): {
                    Any(): {
                        Optional("evpn_vni"): int,
                        Optional("evpn_vni_rd"): str,
                        Optional("evpn_vni_rt"):{
                            Any():{
                                Optional("evpn_vni_rt"): str,
                                Optional("evpn_vni_rt_type"): str,
                            },
                        },
                    },
                },
            },
        },
    }

# ====================================
# Parser for 'show running-config bgp'
# ====================================
class ShowRunningConfigBgp(ShowRunningConfigBgpSchema):
    """Parser for show running-config bgp"""

    cli_command = 'show running-config bgp'

    def cli(self,output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        p1 = re.compile(r'^\s*router +bgp +(?P<bgp_id>[0-9]+)$')
        p2 = re.compile(r'^\s*shutdown$')
        p2_1 = re.compile(r'^\s*evpn$')
        p2_2 = re.compile(r'^\s*vni +(?P<evpn_vni>\d+) +l2$')
        p2_3 = re.compile(r'^\s*rd +(?P<rd>[\w]+)$')
        p2_4 = re.compile(r'^\s*route-target +(?P<evpn_vni_rt_type>[\w]+) +(?P<evpn_vni_rt>[\w\s]+)$')
        p3 = re.compile(r'^\s*vrf +(?P<vrf>[\w\-]+)$')
        p3_1 = re.compile(r'^\s*rd +(?P<rd>[\w]+)$')
        p4 = re.compile(r'^\s*bestpath +(?P<best_path>[a-z\-\s]+)$')
        p5 = re.compile(r'^\s*cluster-id +(?P<cluster_id>[0-9\.]+)$')
        p6 = re.compile(r'^\s*confederation +identifier +(?P<confederation_identifier>[0-9]+)$')
        p7 = re.compile(r'^\s*confederation +peers +(?P<confederation_peers_as>[0-9]+)$')
        p8 = re.compile(r'^\s*no graceful-restart$')
        p9 = re.compile(r'^\s*graceful-restart'
                    r' +(?P<graceful_restart_type>[a-z\-]+)'
                    r' +(?P<time>[0-9]+)$')
        p10 = re.compile(r'^\s*log-neighbor-changes$')
        p11 = re.compile(r'^\s*router-id +(?P<router_id>[0-9\.]+)$')
        p12 = re.compile(r'^\s*timers +bgp +(?P<keepalive_interval>[0-9]+)'
                    r' +(?P<holdtime>[0-9]+)$')
        p13 = re.compile(r'^\s*no enforce-first-as$')
        p14 = re.compile(r'^\s*no fast-external-fallover$')
        p15 = re.compile(r'^\s*dynamic-med-interval +(?P<dynamic_med_interval>[0-9]+)$')
        p16 = re.compile(r'^\s*flush-routes$')
        p17 = re.compile(r'^\s*isolate$')
        p18 = re.compile(r'^\s*disable-policy-batching ipv4 prefix-list +(?P<disable_policy_batching_ipv4>[a-zA-Z0-9]+)$')
        p19 = re.compile(r'^\s*disable-policy-batching ipv6 prefix-list +(?P<disable_policy_batching_ipv6>[a-zA-Z0-9]+)$')
        p20 = re.compile(r'^\s*address-family +(?P<af_name>[a-z0-9\-\s]+)$')
        p21_1 = re.compile(r'^\s*route-target +(?P<af_evpn_vni_rt_type>[\w]+) +(?P<af_evpn_vni_rt>[\w\s]+)$')
        p21 = re.compile(r'^\s*dampening '
                        r'+(?P<af_dampening_half_life_time>[0-9]+) '
                        r'+(?P<af_dampening_reuse_time>[0-9]+) '
                        r'+(?P<af_dampening_suppress_time>[0-9]+) '
                        r'+(?P<af_dampening_max_suppress_time>[0-9]+)$')
        p22 = re.compile(r'^\s*dampening +route-map +(?P<af_dampening_route_map>[A-Z0-9\-\_]+)$')
        p23 = re.compile(r'^\s*nexthop +route-map +(?P<af_nexthop_route_map>[A-Za-z0-9\-\_]+)$')
        p24 = re.compile(r'^\s*nexthop +trigger-delay +critical +(?P<af_nexthop_trigger_delay_critical>[0-9]+) +non-critical +(?P<af_nexthop_trigger_delay_non_critical>[0-9]+)$')
        p25 = re.compile(r'^\s*no nexthop trigger-delay$')
        p26 = re.compile(r'^\s*no client-to-client reflection$')
        p27 = re.compile(r'^\s*distance +(?P<af_distance_extern_as>[0-9]+) +(?P<af_distance_internal_as>[0-9]+) +(?P<af_distance_local>[0-9]+)$')
        p28 = re.compile(r'^\s*maximum-paths( +(?P<af_maximum_paths_type>[a-z]+))? +(?P<af_maximum_paths_value>[0-9]+)$')
        p28_1 = re.compile(r'additional-paths send')
        p28_2 = re.compile(r'additional-paths receive')
        p28_3 = re.compile(r'default-information originate')
        p29 = re.compile(r'^\s*maximum-paths +eibgp +(?P<af_maximum_paths_eibgp>[0-9]+)$')
        p30 = re.compile(r'^\s*aggregate-address +(?P<af_aggregate_address_address>[a-z0-9\.\:]+)(\/(?P<af_aggregate_address_ipv4_mask>[0-9]+))?( +(?P<extra_line>[a-z\-\s]+))?$')
        p31 = re.compile(r'^\s*network +(?P<af_network_number>[0-9\.\:]+)( +mask +(?P<af_network_mask>[0-9\.]+))?( +route-map +(?P<af_network_route_map>[A-Za-z0-9\-\_]+))?$')
        p32 = re.compile(r'^\s*network +(?P<af_network_number>[0-9\.]+)\/(?P<af_network_mask>[0-9]+)( +route-map +(?P<af_network_route_map>[A-Za-z0-9\-\_]+))?$')
        p33 = re.compile(r'^\s*redistribute +isis +(?P<af_redist_isis>[0-9]+) +route-map +(?P<af_redist_isis_route_policy>[A-Za-z0-9\-\_]+)$')
        p34 = re.compile(r'^\s*redistribute +isis +(?P<af_redist_isis>[0-9]+) +route-map +(?P<af_redist_isis_route_policy>[A-Za-z0-9\-\_]+)$')
        p35 = re.compile(r'^\s*redistribute +(ospf|ospfv3) +(?P<af_redist_ospf>[0-9]+) +route-map +(?P<af_redist_ospf_route_policy>[A-Za-z0-9\-\_]+)$')
        p36 = re.compile(r'^\s*redistribute +rip +(?P<af_redist_rip>[0-9]+) +route-map +(?P<af_redist_rip_route_policy>[A-Za-z0-9\-\_]+)$')
        p37 = re.compile(r'^\s*redistribute +static +route-map +(?P<af_redist_static_route_policy>[A-Za-z0-9\-\_]+)$')
        p38 = re.compile(r'^\s*redistribute +direct +route-map +(?P<af_redist_connected_route_policy>[A-Za-z0-9\-\_]+)$')
        p39 = re.compile(r'^\s*allocate-label all$')
        p40 = re.compile(r'^\s*retain route-target all$')
        p41 = re.compile(r'^\s*label-allocation-mode +(?P<per_vrf>[A-Za-z0-9]+)$')
        p103 = re.compile(r'^\s*advertise-pip$')
        p42 = re.compile(r'^\s*neighbor +(?P<neighbor_id>[a-z0-9\.\:]+)$')
        p43 = re.compile(r'^\s*bfd$')
        p44 = re.compile(r'^\s*capability suppress 4-byte-as$')
        p45 = re.compile(r'^\s*description +(?P<nbr_description>.+)$')
        p46 = re.compile(r'^\s*disable-connected-check$')
        p47 = re.compile(r'^\s*ebgp-multihop +(?P<nbr_ebgp_multihop_max_hop>[0-9]+)$')
        p48 = re.compile(r'^\s*inherit peer-session +(?P<nbr_inherit_peer_session>[A-Za-z0-9\-]+)$')
        p49 = re.compile(r'^\s*local-as +(?P<nbr_local_as_as_no>[0-9\.]+)( +(?P<no_prepend>no-prepend)( +(?P<replace_as>replace-as)( +(?P<dual_as>dual-as))?)?)?$')
        p50 = re.compile(r'^\s*remote-as +(?P<nbr_remote_as>[0-9]+)$')
        p51 = re.compile(r'^\s*remove-private-as$')
        p52 = re.compile(r'^\s*shutdown$')
        p53 = re.compile(r'^\s*timers +(?P<nbr_keepalive_interval>[0-9]+) +(?P<nbr_holdtime>[0-9]+)$')
        p54 = re.compile(r'^\s*update-source +(?P<nbr_update_source>[A-Za-z0-9\/\.]+)$')
        p55 = re.compile(r'^\s*password +(?P<nbr_password_text>.*)$')
        p56 = re.compile(r'^\s*transport connection-mode +(?P<nbr_transport_connection_mode>[a-z]+)$')
        p101 = re.compile(r'^\s*peer-type +(?P<nbr_peer_type>[\w\-]+)$')
        p104 = re.compile(r'^\s*inherit peer +(?P<nbr_inherit_peer>\S+)$')
        p57 = re.compile(r'^\s*address-family +(?P<nbr_af_name>[A-Za-z0-9\s\-]+)$')
        p58 = re.compile(r'^\s*allowas-in( +(?P<nbr_af_allowas_in_as_number>[0-9]+))?$')
        p59 = re.compile(r'^\s*inherit peer-policy +(?P<nbr_af_inherit_peer_policy>[A-Za-z0-9\-]+) +(?P<nbr_af_inherit_peer_seq>[0-9]+)$')
        p60 = re.compile(r'^\s*maximum-prefix +(?P<nbr_af_maximum_prefix_max_prefix_no>[0-9]+)( +(?P<nbr_af_maximum_prefix_threshold>[0-9]+))?( +restart +(?P<nbr_af_maximum_prefix_restart>[0-9]+))?$')
        p61 = re.compile(r'^\s*maximum-prefix +(?P<nbr_af_maximum_prefix_max_prefix_no>[0-9]+)( +(?P<nbr_af_maximum_prefix_threshold>[0-9]+))?( +(?P<nbr_af_maximum_prefix_warning_only>warning-only))?$')
        p62 = re.compile(r'^\s*(?:no )?route-map +(?P<nbr_af_route_map_name_in>.*) in$')
        p63 = re.compile(r'^\s*(?:no )?route-map +(?P<nbr_af_route_map_name_out>.*) out$')
        p64 = re.compile(r'^\s*route-reflector-client$')
        p65 = re.compile(r'^\s*send-community$')
        p66 = re.compile(r'^\s*send-community +extended$')
        p100 = re.compile(r'^\s*rewrite-evpn-rt-asn$')
        p67 = re.compile(r'^\s*soft-reconfiguration inbound( +(?P<nbr_af_soft_reconfiguration_extra>.*))?$')
        p68 = re.compile(r'^\s*next-hop-self$')
        p69 = re.compile(r'^\s*as-override$')
        p70 = re.compile(r'^\s*default-originate( +route-map +(?P<nbr_af_default_originate_route_map>.*))?$')
        p71 = re.compile(r'^\s*soo +(?P<nbr_af_soo>.*)$')
        p72 = re.compile(r'^\s*template peer-session +(?P<ps_name>.*)$')
        p73 = re.compile(r'^\s*bfd$')
        p74 = re.compile(r'^\s*bfd$')
        p75 = re.compile(r'^\s*description +(?P<ps_description>.*)$')
        p76 = re.compile(r'^\s*disable-connected-check$')
        p77 = re.compile(r'^\s*ebgp-multihop +(?P<ps_ebgp_multihop_max_hop>[0-9]+)$$')
        p78 = re.compile(r'^\s*local-as +(?P<ps_local_as_as_no>[0-9\.]+)( +no-prepend( +replace-as( +dual-as)?)?)?$')
        p79 = re.compile(r'^\s*password +(?P<ps_password_text>.*)$')
        p80 = re.compile(r'^\s*remote-as +(?P<ps_remote_as>[0-9]+)$')
        p81 = re.compile(r'^\s*shutdown$')
        p82 = re.compile(r'^\s*timers +(?P<ps_keepalive_interval>[0-9]+) +(?P<ps_hodltime>[0-9]+)$')
        p83 = re.compile(r'^\s*transport connection-mode +(?P<ps_transport_connection_mode>[a-z]+)$')
        p84 = re.compile(r'^\s*update-source +(?P<ps_update_source>[A-Za-z0-9\/\.]+)$')
        p85 = re.compile(r'^\s*template peer-policy +(?P<pp_name>.*)$')
        p86 = re.compile(r'^\s*allowas-in( +(?P<pp_allowas_in_as_number>[0-9]+))?$')
        p87 = re.compile(r'^\s*as-override$')
        p88 = re.compile(r'^\s*default-originate( +route-map +(?P<pp_default_originate_route_map>.*))?$')
        p89 = re.compile(r'^\s*route-map +(?P<pp_route_map_name_in>.*) in$')
        p90 = re.compile(r'^\s*route-map +(?P<pp_route_map_name_out>.*) out$')
        p91 = re.compile(r'^\s*maximum-prefix +(?P<pp_maximum_prefix_max_prefix_no>[0-9]+)( +(?P<nbr_af_maximum_prefix_threshold>[0-9]+))?(restart +(?P<nbr_af_maximum_prefix_restart>[0-9]+))?$')
        p92 = re.compile(r'^\s*maximum-prefix +(?P<pp_maximum_prefix_max_prefix_no>[0-9]+)( +(?P<pp_maximum_prefix_threshold>[0-9]+))?( +(?P<pp_maximum_prefix_warning_only>warning-only))?$')
        p93 = re.compile(r'^\s*next-hop-self$')
        p94 = re.compile(r'^\s*route-reflector-client$')
        p95 = re.compile(r'^\s*send-community$')
        p96 = re.compile(r'^\s*send-community +extended$')
        p97 = re.compile(r'^\s*soft-reconfiguration inbound( +(?P<nbr_af_soft_reconfiguration_extra>.*))?$')
        p98 = re.compile(r'^\s*soo +(?P<pp_soo>.*)$')
        peer_1 = re.compile(r'template peer +(?P<peer_name>\S+)')
        # Init vars
        bgp_dict = {}
        bgp_id = ''
        protocol_shutdown = False
        send_community_standard_match = 'False'
        peer_policy_send_community_standard_match = 'False'
        neighbor_id = ''
        af_name = ''
        nbr_af_name = ''
        ps_name = ''
        pp_name = ''
        peer_name = ''
        vni_flag = False

        for line in out.splitlines():
            line = line.strip()
            # router bgp 333
            m = p1.match(line)
            if m:
                # Coversion to BGP ASN 4260036636(AS-PLAIN) from 65003.28(AS-COLON)
                bgp_id = m.groupdict()['bgp_id']
                if '.' in bgp_id:
                    val = bgp_id.split('.')
                    bgp_id = 65536*int(val[0])+int(val[1])
                else:
                    bgp_id = int(bgp_id)

                if 'bgp' not in bgp_dict:
                    bgp_dict['bgp'] = {}
                if 'instance' not in bgp_dict['bgp']:
                    bgp_dict['bgp']['instance'] = {}
                if 'default' not in bgp_dict['bgp']['instance']:
                    bgp_dict['bgp']['instance']['default'] = {}
                bgp_dict['bgp']['instance']['default']['bgp_id'] = bgp_id
                bgp_dict['bgp']['instance']['default']['protocol_shutdown'] = \
                    protocol_shutdown
                vrf = 'default'
                if 'vrf' not in bgp_dict['bgp']['instance']['default']:
                    bgp_dict['bgp']['instance']['default']['vrf'] = {}
                if vrf not in bgp_dict['bgp']['instance']['default']['vrf']:
                    bgp_dict['bgp']['instance']['default']['vrf'][vrf] = {}
                    bgp_vrf_default_dict = bgp_dict['bgp']['instance']['default']['vrf'][vrf]
                continue

            if bgp_id:
                #   shutdown
                m = p2.match(line)
                if m:
                    bgp_dict['bgp']['instance']['default']['protocol_shutdown'] = True
                    continue

                # evpn
                m = p2_1.match(line)
                if m:
                    if 'vxlan' not in bgp_dict:
                        bgp_dict['vxlan'] = {}
                    if 'evpn' not in bgp_dict['vxlan']:
                        bgp_dict['vxlan']['evpn'] = {}
                    continue

                # vni 5001 l2
                m = p2_2.match(line)
                if m:
                    vni_flag = True
                    if 'evpn_vni' not in bgp_dict['vxlan']['evpn']:
                        bgp_dict['vxlan']['evpn']['evpn_vni'] = {}
                    evpn_vni = int(m.groupdict()['evpn_vni'])
                    if evpn_vni not in  bgp_dict['vxlan']['evpn']['evpn_vni']:
                        bgp_dict['vxlan']['evpn']['evpn_vni'][evpn_vni] = {}
                    bgp_dict['vxlan']['evpn']['evpn_vni'][evpn_vni]['evpn_vni'] = evpn_vni
                    continue

                if vni_flag:
                    # rd auto
                    m = p2_3.match(line)
                    if m:
                        bgp_dict['vxlan']['evpn']['evpn_vni'][evpn_vni]['evpn_vni_rd'] = m.groupdict()['rd']
                        continue

                    # route-target import auto
                    # route-target export auto
                    m = p2_4.match(line)
                    if m:
                        evpn_vni_rt = m.groupdict()['evpn_vni_rt']
                        if 'evpn_vni_rt' not in bgp_dict['vxlan']['evpn']['evpn_vni'][evpn_vni]:
                            bgp_dict['vxlan']['evpn']['evpn_vni'][evpn_vni]['evpn_vni_rt'] = {}
                        if evpn_vni_rt not in bgp_dict['vxlan']['evpn']['evpn_vni'][evpn_vni]['evpn_vni_rt']:
                            bgp_dict['vxlan']['evpn']['evpn_vni'][evpn_vni]['evpn_vni_rt'][evpn_vni_rt] = {}
                            bgp_vni_rt_dict = \
                                bgp_dict['vxlan']['evpn']['evpn_vni'][evpn_vni]['evpn_vni_rt'][evpn_vni_rt]

                        bgp_vni_rt_dict['evpn_vni_rt_type'] = m.groupdict()['evpn_vni_rt_type']
                        bgp_vni_rt_dict['evpn_vni_rt'] = evpn_vni_rt
                        continue

                # vrf VRF1
                m = p3.match(line)
                if m:
                    # Get keys
                    vrf = str(m.groupdict()['vrf'])
                    af_name = ''
                    neighbor_id = ''
                    nbr_af_name = ''
                    vni_flag = False
                    if 'vrf' not in bgp_dict['bgp']['instance']['default']:
                        bgp_dict['bgp']['instance']['default']['vrf'] = {}
                    if vrf not in bgp_dict['bgp']['instance']['default']['vrf']:
                        if len(bgp_dict['bgp']['instance']['default']['vrf']['default']) == 0:
                            bgp_dict['bgp']['instance']['default']['vrf'].pop("default", None)
                        bgp_dict['bgp']['instance']['default']['vrf'][vrf] = {}
                        bgp_vrf_nondefault_dict = bgp_dict['bgp']['instance']['default']['vrf'][vrf]
                    continue

                if vrf:
                    if vrf == 'default':
                        bgp_vrf_dict = bgp_vrf_default_dict
                    else:
                        bgp_vrf_dict = bgp_vrf_nondefault_dict

                    # rd auto
                    m = p3_1.match(line)
                    if m:
                        bgp_vrf_dict['rd'] = m.groupdict()['rd']
                        continue

                    #   bestpath cost-community ignore
                    #   bestpath compare-routerid
                    #   bestpath med missing-as-worst
                    #   bestpath always-compare-med
                    m = p4.match(line)
                    if m:
                        # Get keys
                        best_path = str(m.groupdict()['best_path'])
                        # Initialize variables
                        bgp_vrf_dict['always_compare_med'] = False
                        bgp_vrf_dict['bestpath_compare_routerid'] = False
                        bgp_vrf_dict['bestpath_cost_community_ignore'] = False
                        bgp_vrf_dict['bestpath_med_missing_at_worst'] = False
                        if best_path == 'cost-community ignore':
                            bgp_vrf_dict['bestpath_cost_community_ignore'] = True
                        elif best_path == 'compare-routerid':
                            bgp_vrf_dict['bestpath_compare_routerid'] = True
                        elif best_path == 'med missing-as-worst':
                            bgp_vrf_dict['bestpath_med_missing_at_worst'] = True
                        elif best_path == 'always-compare-med':
                            bgp_vrf_dict['always_compare_med'] = True
                        continue

                    #   cluster-id <cluster_id>
                    m = p5.match(line)
                    if m:
                        bgp_vrf_dict['cluster_id'] = str(m.groupdict()['cluster_id'])
                        continue

                    #   confederation identifier <confederation_identifier>
                    m = p6.match(line)
                    if m:
                        bgp_vrf_dict['confederation_identifier'] = \
                            int(m.groupdict()['confederation_identifier'])
                        continue

                    #   confederation peers <confederation_peers_as>
                    m = p7.match(line)
                    if m:
                        bgp_vrf_dict['confederation_peers_as'] = \
                            str(m.groupdict()['confederation_peers_as'])
                        continue

                    #   no graceful-restart
                    m = p8.match(line)
                    if m:
                        bgp_vrf_dict['graceful_restart'] = False
                        continue
                    elif 'graceful_restart' not in bgp_vrf_dict:
                        bgp_vrf_dict['graceful_restart'] = True

                    #   graceful-restart restart-time 121
                    #   graceful-restart stalepath-time 301
                    m = p9.match(line)
                    if m:
                        graceful_restart_type = str(m.groupdict()['graceful_restart_type'])
                        if graceful_restart_type == 'restart-time':
                            bgp_vrf_dict['graceful_restart_restart_time'] = \
                                    int(m.groupdict()['time'])
                        else:
                            bgp_vrf_dict['graceful_restart_stalepath_time'] = \
                                    int(m.groupdict()['time'])
                        continue

                    #   log-neighbor-changes
                    m = p10.match(line)
                    if m:
                        bgp_vrf_dict['log_neighbor_changes'] = True
                        continue
                    elif 'log_neighbor_changes' not in bgp_vrf_dict:
                        bgp_vrf_dict['log_neighbor_changes'] = False

                    #   router-id <router-id>
                    m = p11.match(line)
                    if m:
                        bgp_vrf_dict['router_id'] = str(m.groupdict()['router_id'])
                        continue

                    #   timers bgp <keepalive-interval> <holdtime>
                    m = p12.match(line)
                    if m:
                        bgp_vrf_dict['keepalive_interval'] = int(m.groupdict()['keepalive_interval'])
                        bgp_vrf_dict['holdtime'] = int(m.groupdict()['holdtime'])
                        continue

                    #   no enforce-first-as
                    m = p13.match(line)
                    if m:
                        bgp_vrf_dict['enforce_first_as'] = False
                        continue
                    elif 'enforce_first_as' not in bgp_vrf_dict:
                        bgp_vrf_dict['enforce_first_as'] = True

                    #   no fast-external-fallover
                    m = p14.match(line)
                    if m:
                        bgp_vrf_dict['fast_external_fallover'] = False
                        continue
                    elif 'fast_external_fallover' not in bgp_vrf_dict:
                        bgp_vrf_dict['fast_external_fallover'] = True

                    #   dynamic-med-interval 70
                    m = p15.match(line)
                    if m:
                        bgp_vrf_dict['dynamic_med_interval'] = \
                            int(m.groupdict()['dynamic_med_interval'])
                        continue

                    #   flush-routes
                    m = p16.match(line)
                    if m:
                        bgp_vrf_dict['flush_routes'] = True
                        continue
                    elif 'flush_routes' not in bgp_vrf_dict:
                        bgp_vrf_dict['flush_routes'] = False

                    #   isolate
                    m = p17.match(line)
                    if m:
                        bgp_vrf_dict['isolate'] = True
                        continue
                    elif 'isolate' not in bgp_vrf_dict:
                        bgp_vrf_dict['isolate'] = False

                    #   disable-policy-batching ipv4 prefix-list <WORD>
                    m = p18.match(line)
                    if m:
                        bgp_vrf_dict['disable_policy_batching_ipv4'] = \
                            str(m.groupdict()['disable_policy_batching_ipv4'])
                        continue

                    #   disable-policy-batching ipv4 prefix-list <WORD>
                    m = p19.match(line)
                    if m:
                        bgp_vrf_dict['disable_policy_batching_ipv6'] = \
                            str(m.groupdict()['disable_policy_batching_ipv6'])
                        continue

                    if neighbor_id == '' and peer_name == '' or \
                            'af_name' not in bgp_dict['bgp']['instance']['default']['vrf'][vrf]:
                        #   address-family ipv4 multicast
                        m = p20.match(line)
                        if m:
                            # Get keys
                            af_name = str(m.groupdict()['af_name'])
                            if 'af_name' not in bgp_vrf_dict:
                                bgp_dict['bgp']['instance']['default']['vrf'][vrf]['af_name'] = {}
                            if af_name not in bgp_dict['bgp']['instance']['default']['vrf'][vrf]['af_name']:
                                bgp_dict['bgp']['instance']['default']['vrf'][vrf]['af_name'][af_name] = {}
                                bgp_af_dict = bgp_dict['bgp']['instance']['default']['vrf'][vrf]['af_name'][af_name]
                            continue

                    if af_name:
                        # route-target both auto
                        # route-target both auto evpn
                        m = p21_1.match(line)
                        if m:
                            bgp_af_dict['af_evpn_vni_rt_type'] = m.groupdict()['af_evpn_vni_rt_type']
                            bgp_af_dict['af_evpn_vni_rt'] = m.groupdict()['af_evpn_vni_rt']

                        #    dampening [ { <af_dampening_half_life_time>
                        #    <af_dampening_resuse_time> <af_dampening_suppress_time>
                        #    <af_dampening_max_suppress_time> } |
                        #    { route-map <af_dampening_route_map> } ]
                        m = p21.match(line)
                        if m:
                            bgp_af_dict['af_dampening'] = True
                            bgp_af_dict['af_dampening_half_life_time'] = \
                                int(m.groupdict()['af_dampening_half_life_time'])
                            bgp_af_dict['af_dampening_reuse_time'] = \
                                int(m.groupdict()['af_dampening_reuse_time'])
                            bgp_af_dict['af_dampening_suppress_time'] = \
                                int(m.groupdict()['af_dampening_suppress_time'])
                            bgp_af_dict['af_dampening_max_suppress_time'] = \
                                int(m.groupdict()['af_dampening_max_suppress_time'])
                            continue

                        #    dampening [ { route-map <af_dampening_route_map> } ]
                        m = p22.match(line)
                        if m:
                            bgp_af_dict['af_dampening'] = True
                            bgp_af_dict['af_dampening_route_map'] = str(m.groupdict()['af_dampening_route_map'])
                            continue

                        #    nexthop route-map <af_nexthop_route_map>
                        m = p23.match(line)
                        if m:
                            bgp_af_dict['af_nexthop_route_map'] = str(m.groupdict()['af_nexthop_route_map'])
                            continue

                        #     { nexthop trigger-delay critical
                        #     <af_nexthop_trigger_delay_critical> non-critical
                        #     <af_nexthop_trigger_delay_non_critical> } |
                        #     { no nexthop trigger-delay }
                        m = p24.match(line)
                        if m:
                            bgp_af_dict['af_nexthop_trigger_enable'] = True
                            bgp_af_dict['af_nexthop_trigger_delay_critical'] = \
                                int(m.groupdict()['af_nexthop_trigger_delay_critical'])
                            bgp_af_dict['af_nexthop_trigger_delay_non_critical'] = \
                                int(m.groupdict()['af_nexthop_trigger_delay_non_critical'])
                            continue

                        #     {no nexthop trigger-delay }
                        m = p25.match(line)
                        if m:
                            bgp_af_dict['af_nexthop_trigger_enable'] = False
                            continue

                        #     {no client-to-client reflection }
                        m = p26.match(line)
                        if m:
                            bgp_af_dict['af_client_to_client_reflection'] = False
                            continue
                        elif 'af_client_to_client_reflection' not in bgp_af_dict:
                            bgp_af_dict['af_client_to_client_reflection'] = True

                        #    distance <af_distance_extern_as> <af_distance_internal_as> <af_distance_local> | no distance [ <af_distance_extern_as> <af_distance_internal_as> <af_distance_local> ]
                        m = p27.match(line)
                        if m:
                            bgp_af_dict['af_distance_extern_as'] = int(m.groupdict()['af_distance_extern_as'])
                            bgp_af_dict['af_distance_internal_as'] = int(m.groupdict()['af_distance_internal_as'])
                            bgp_af_dict['af_distance_local'] = int(m.groupdict()['af_distance_local'])
                            continue

                        #    maximum-paths <af_maximum_paths_ebgp>
                        #    maximum-paths ibgp <af_maximum_paths_ibgp>
                        m = p28.match(line)
                        if m:
                            if m.groupdict()['af_maximum_paths_type']:
                                bgp_af_dict['af_maximum_paths_ibgp'] = int(m.groupdict()['af_maximum_paths_value'])
                            else:
                                bgp_af_dict['af_maximum_paths_ebgp'] = int(m.groupdict()['af_maximum_paths_value'])
                            continue

                        #   additional-paths send
                        m = p28_1.match(line)
                        if m:
                            bgp_af_dict['af_additional_paths_send'] = True
                            continue

                        #   additional-paths receive
                        m = p28_2.match(line)
                        if m:
                            bgp_af_dict['af_additional_paths_receive'] = True
                            continue

                        # default-information originate
                        m = p28_3.match(line)
                        if m:
                            bgp_af_dict['af_default_originate'] = True
                            continue

                        #    maximum-paths eibgp <af_maximum_paths_eibgp>
                        m = p29.match(line)
                        if m:
                            bgp_af_dict['af_maximum_paths_eibgp'] = int(m.groupdict()['af_maximum_paths_eibgp'])
                            continue

                        #    aggregate-address <af_aggregate_address_ipv4_address>/<af_aggregate_address_ipv4_mask> [ as-set | summary-only ] +
                        #    aggregate-address <af_v6_aggregate_address_ipv6_address> [ as-set | summary-only ] +
                        m = p30.match(line)
                        if m:
                            ip_address = str(m.groupdict()['af_aggregate_address_address'])
                            if '::' not in ip_address:
                                bgp_af_dict['af_aggregate_address_ipv4_address'] = ip_address
                                bgp_af_dict['af_aggregate_address_ipv4_mask'] = \
                                    int(m.groupdict()['af_aggregate_address_ipv4_mask'])
                                if m.groupdict()['extra_line']:
                                    if m.groupdict()['extra_line'] == 'as-set':
                                        bgp_af_dict['af_aggregate_address_as_set'] = True
                                    elif m.groupdict()['extra_line'] == 'summary-only':
                                        bgp_af_dict['af_aggregate_address_summary_only'] = True
                                    elif m.groupdict()['extra_line'] == 'as-set summary-only':
                                        bgp_af_dict['af_aggregate_address_as_set'] = True
                                        bgp_af_dict['af_aggregate_address_summary_only'] = True
                            else:
                                bgp_af_dict['af_v6_aggregate_address_ipv6_address'] = ip_address
                                if m.groupdict()['extra_line']:
                                    if m.groupdict()['extra_line'] == 'as-set':
                                        bgp_af_dict['af_v6_aggregate_address_as_set'] = True
                                    elif m.groupdict()['extra_line'] == 'summary-only':
                                        bgp_af_dict['af_v6_aggregate_address_summary_only'] = True
                                    elif m.groupdict()['extra_line'] == 'as-set summary-only':
                                        bgp_af_dict['af_v6_aggregate_address_as_set'] = True
                                        bgp_af_dict['af_v6_aggregate_address_summary_only'] = True
                            continue

                        #    network { <af_network_number> mask <af_network_mask> } [ route-map <rmap-name> ] +
                        #    network <af_v6_network_number> [ route-map <af_v6_network_route_map> ] +
                        m = p31.match(line)
                        if m:
                            if m.groupdict()['af_network_mask']:
                                bgp_af_dict['af_network_number'] = str(m.groupdict()['af_network_number'])
                                bgp_af_dict['af_network_mask'] = int(m.groupdict()['af_network_mask'])
                                if m.groupdict()['af_network_route_map']:
                                    bgp_af_dict['af_network_route_map'] = str(m.groupdict()['af_network_route_map'])
                            else:
                                bgp_af_dict['af_v6_network_number'] = str(m.groupdict()['af_network_number'])
                                if m.groupdict()['af_network_route_map']:
                                    bgp_af_dict['af_v6_network_route_map'] = str(m.groupdict()['af_network_route_map'])
                            continue

                        #    network { <af_network_number>/<ip-prefix> } [ route-map <rmap-name> ] +
                        m = p32.match(line)
                        if m:
                            group = m.groupdict()
                            if 'af_network_number' in bgp_af_dict:
                                if not isinstance(bgp_af_dict['af_network_number'], list):
                                    bgp_af_dict['af_network_number'] = [bgp_af_dict['af_network_number']]
                                bgp_af_dict['af_network_number'].append(group['af_network_number'])
                            else:
                                bgp_af_dict.update({'af_network_number': group['af_network_number']})
                            
                            if 'af_network_mask' in bgp_af_dict:
                                if not isinstance(bgp_af_dict['af_network_mask'], list):
                                    bgp_af_dict['af_network_mask'] = [bgp_af_dict['af_network_mask']]
                                bgp_af_dict['af_network_mask'].append(int(group['af_network_mask']))
                            else:
                                bgp_af_dict.update({'af_network_mask': int(group['af_network_mask'])})
                                
                            if m.groupdict()['af_network_route_map']:
                                bgp_af_dict['af_network_route_map'] = str(m.groupdict()['af_network_route_map'])
                            continue

                        #    redistribute isis <Isis.pid> route-map <route_policy>
                        m = p33.match(line)
                        if m:
                            bgp_af_dict['af_redist_isis'] = str(m.groupdict()['af_redist_isis'])
                            bgp_af_dict['af_redist_isis_route_policy'] = \
                                str(m.groupdict()['af_redist_isis_route_policy'])
                            continue

                        #    redistribute isis <Isis.pid> route-map <route_policy>
                        m = p34.match(line)
                        if m:
                            bgp_af_dict['af_redist_isis'] = str(m.groupdict()['af_redist_isis'])
                            bgp_af_dict['af_redist_isis_route_policy'] = \
                                str(m.groupdict()['af_redist_isis_route_policy'])
                            continue

                        #    redistribute ospf <Ospf.pid> route-map <route_policy>
                        #    redistribute ospfv3 <Ospf.pid> route-map <route_policy>
                        m = p35.match(line)
                        if m:
                            bgp_af_dict['af_redist_ospf'] = str(m.groupdict()['af_redist_ospf'])
                            bgp_af_dict['af_redist_ospf_route_policy'] = \
                                str(m.groupdict()['af_redist_ospf_route_policy'])
                            continue

                        #    Redistribute rip <Rip.pid> route-map <route_policy>
                        m = p36.match(line)
                        if m:
                            bgp_af_dict['af_redist_rip'] = str(m.groupdict()['af_redist_rip'])
                            bgp_af_dict['af_redist_rip_route_policy'] = \
                                str(m.groupdict()['af_redist_rip_route_policy'])
                            continue

                        #    redistribute static route-map <route_policy>
                        m = p37.match(line)
                        if m:
                            bgp_af_dict['af_redist_static'] = True
                            bgp_af_dict['af_redist_static_route_policy'] = \
                                str(m.groupdict()['af_redist_static_route_policy'])
                            continue

                        #    redistribute direct route-map <route_policy>
                        m = p38.match(line)
                        if m:
                            bgp_af_dict['af_redist_connected'] = True
                            bgp_af_dict['af_redist_connected_route_policy'] = \
                                str(m.groupdict()['af_redist_connected_route_policy'])
                            continue

                        #    allocate-label all
                        m = p39.match(line)
                        if m:
                            bgp_af_dict['af_v6_allocate_label_all'] = True
                            continue

                        #    retain route-target all
                        m = p40.match(line)
                        if m:
                            bgp_af_dict['af_retain_rt_all'] = True
                            continue

                        #    label-allocation-mode per-vrf
                        m = p41.match(line)
                        if m:
                            bgp_af_dict['af_label_allocation_mode'] = str(m.groupdict()['per_vrf'])
                            continue

                        #    advertise-pip
                        m = p103.match(line)
                        if m:
                            bgp_af_dict['af_advertise_pip'] = True
                            continue
                    #   neighbor <neighbor_id>
                    m = p42.match(line)
                    if m:
                        # Get keys
                        neighbor_id = str(m.groupdict()['neighbor_id'])
                        if 'neighbor_id' not in bgp_dict['bgp']['instance']['default']['vrf'][vrf]:
                            bgp_dict['bgp']['instance']['default']['vrf'][vrf]['neighbor_id'] = {}
                        if neighbor_id not in bgp_dict['bgp']['instance']['default']['vrf'][vrf]['neighbor_id']:
                            bgp_dict['bgp']['instance']['default']['vrf'][vrf]['neighbor_id'][neighbor_id] = {}
                            bgp_vrf_neighbor_dict = \
                                bgp_dict['bgp']['instance']['default']['vrf'][vrf]['neighbor_id'][neighbor_id]
                        continue

                    #   Same line of configuration can be configured under the peer session section
                    if neighbor_id:
                        #   bfd
                        m = p43.match(line)
                        if m:
                            bgp_vrf_neighbor_dict['nbr_fall_over_bfd'] = True
                            continue
                        elif 'nbr_fall_over_bfd' not in bgp_vrf_neighbor_dict:
                            bgp_vrf_neighbor_dict['nbr_fall_over_bfd'] = False

                        #   capability suppress 4-byte-as
                        m = p44.match(line)
                        if m:
                            bgp_vrf_neighbor_dict['nbr_suppress_four_byte_as_capability'] = True
                            continue
                        elif 'nbr_suppress_four_byte_as_capability' not in bgp_vrf_neighbor_dict:
                            bgp_vrf_neighbor_dict['nbr_suppress_four_byte_as_capability'] = False

                        #   description <nbr_description>
                        m = p45.match(line)
                        if m:
                            bgp_vrf_neighbor_dict['nbr_description'] = \
                                str(m.groupdict()['nbr_description'])
                            continue

                        #   disable-connected-check
                        m = p46.match(line)
                        if m:
                            bgp_vrf_neighbor_dict['nbr_disable_connected_check'] = True
                            continue
                        elif 'nbr_disable_connected_check' not in bgp_vrf_neighbor_dict:
                            bgp_vrf_neighbor_dict['nbr_disable_connected_check'] = False

                        #   ebgp-multihop <nbr_ebgp_multihop_max_hop>
                        m = p47.match(line)
                        if m:
                            bgp_vrf_neighbor_dict['nbr_ebgp_multihop'] = True
                            bgp_vrf_neighbor_dict['nbr_ebgp_multihop_max_hop'] = \
                                int(m.groupdict()['nbr_ebgp_multihop_max_hop'])
                            continue
                        elif 'nbr_ebgp_multihop' not in bgp_vrf_neighbor_dict:
                            bgp_vrf_neighbor_dict['nbr_ebgp_multihop'] = False

                        #   inherit peer-session <nbr_inherit_peer_session>
                        m = p48.match(line)
                        if m:
                            bgp_vrf_neighbor_dict['nbr_inherit_peer_session'] = \
                                str(m.groupdict()['nbr_inherit_peer_session'])
                            continue

                        #    { local-as <nbr_local_as_as_no> [ no-prepend [ replace-as [ dual-as ] ] ] }
                        m = p49.match(line)
                        if m:
                            bgp_vrf_neighbor_dict['nbr_local_as_as_no'] = \
                                int(m.groupdict()['nbr_local_as_as_no'])
                            if 'nbr_local_as_no_prepend' in m.groupdict():
                                bgp_vrf_neighbor_dict['nbr_local_as_no_prepend'] = True
                                bgp_vrf_neighbor_dict['nbr_local_as_replace_as'] = True
                                bgp_vrf_neighbor_dict['nbr_local_as_dual_as'] = True
                            continue
                        elif 'nbr_local_as_no_prepend' not in bgp_vrf_neighbor_dict:
                            bgp_vrf_neighbor_dict['nbr_local_as_no_prepend'] = False
                            bgp_vrf_neighbor_dict['nbr_local_as_replace_as'] = False
                            bgp_vrf_neighbor_dict['nbr_local_as_dual_as'] = False

                        #   { remote-as <nbr_remote_as> }
                        m = p50.match(line)
                        if m:
                            bgp_vrf_neighbor_dict['nbr_remote_as'] = \
                                int(m.groupdict()['nbr_remote_as'])
                            continue

                        #   remove-private-as
                        m = p51.match(line)
                        if m:
                            bgp_vrf_neighbor_dict['nbr_remove_private_as'] = True
                            continue
                        elif 'nbr_remove_private_as' not in bgp_vrf_neighbor_dict:
                            bgp_vrf_neighbor_dict['nbr_remove_private_as'] = False

                        #   shutdown
                        m = p52.match(line)
                        if m:
                            bgp_vrf_neighbor_dict['nbr_shutdown'] = True
                            continue
                        elif 'nbr_shutdown' not in bgp_vrf_neighbor_dict:
                            bgp_vrf_neighbor_dict['nbr_shutdown'] = False

                        #   timers <nbr_keepalive_interval> <nbr_holdtime>
                        m = p53.match(line)
                        if m:
                            bgp_vrf_neighbor_dict['nbr_keepalive_interval'] = \
                                int(m.groupdict()['nbr_keepalive_interval'])
                            bgp_vrf_neighbor_dict['nbr_holdtime'] = \
                                int(m.groupdict()['nbr_holdtime'])
                            continue

                        #   update-source <nbr_update_source>
                        m = p54.match(line)
                        if m:
                            bgp_vrf_neighbor_dict['nbr_update_source'] = \
                                str(m.groupdict()['nbr_update_source'])
                            continue

                        #   password <nbr_password_text>
                        m = p55.match(line)
                        if m:
                            bgp_vrf_neighbor_dict['nbr_password_text'] = \
                                str(m.groupdict()['nbr_password_text'])
                            continue

                        #   transport connection-mode <nbr_transport_connection_mode>
                        m = p56.match(line)
                        if m:
                            bgp_vrf_neighbor_dict['nbr_transport_connection_mode'] = \
                                str(m.groupdict()['nbr_transport_connection_mode'])
                            continue

                        # peer-type fabric-external
                        m = p101.match(line)
                        if m:
                            bgp_vrf_neighbor_dict\
                                ['nbr_peer_type'] = m.groupdict()['nbr_peer_type']
                            continue

                        # inherit peer GENIE-NEXUS-EBGP
                        m = p104.match(line)
                        if m:
                            bgp_vrf_neighbor_dict\
                                ['nbr_inherit_peer'] = m.groupdict()['nbr_inherit_peer']
                            continue

                        #   address-family <nbr_af_name>
                        m = p57.match(line)
                        if m:
                            nbr_af_name = str(m.groupdict()['nbr_af_name'])
                            if 'nbr_af_name' not in bgp_vrf_neighbor_dict:
                                bgp_vrf_neighbor_dict['nbr_af_name'] = {}
                            if nbr_af_name not in bgp_vrf_neighbor_dict['nbr_af_name']:
                                bgp_vrf_neighbor_dict['nbr_af_name'][nbr_af_name] = {}
                                bgp_vrf_af_dict = bgp_vrf_neighbor_dict['nbr_af_name'][nbr_af_name]
                            continue

                        if 'nbr_af_name' in bgp_vrf_neighbor_dict:
                            #   allowas-in [ <allowas-in-cnt> ]
                            m = p58.match(line)
                            if m:
                                bgp_vrf_af_dict['nbr_af_allowas_in'] = True
                                if m.groupdict()['nbr_af_allowas_in_as_number']:
                                    bgp_vrf_af_dict['nbr_af_allowas_in_as_number'] = \
                                        int(m.groupdict()['nbr_af_allowas_in_as_number'])
                                continue
                            elif 'nbr_af_allowas_in' not in bgp_vrf_af_dict:
                                bgp_vrf_af_dict['nbr_af_allowas_in'] = False

                            #   inherit peer-policy <nbr_af_inherit_peer_policy> <nbr_af_inherit_peer_seq>
                            m = p59.match(line)
                            if m:
                                bgp_vrf_af_dict['nbr_af_inherit_peer_policy'] = \
                                    str(m.groupdict()['nbr_af_inherit_peer_policy'])
                                bgp_vrf_af_dict['nbr_af_inherit_peer_seq'] = \
                                    int(m.groupdict()['nbr_af_inherit_peer_seq'])
                                continue

                            #   maximum-prefix <nbr_af_maximum_prefix_max_prefix_no> [ <nbr_af_maximum_prefix_threshold> ] [ restart <nbr_af_maximum_prefix_restart> ]
                            m = p60.match(line)
                            if m:
                                bgp_vrf_af_dict['nbr_af_maximum_prefix_max_prefix_no'] = \
                                    int(m.groupdict()['nbr_af_maximum_prefix_max_prefix_no'])
                                if m.groupdict()['nbr_af_maximum_prefix_threshold']:
                                    bgp_vrf_af_dict['nbr_af_maximum_prefix_threshold'] = \
                                        int(m.groupdict()['nbr_af_maximum_prefix_threshold'])
                                if m.groupdict()['nbr_af_maximum_prefix_restart']:
                                    bgp_vrf_af_dict['nbr_af_maximum_prefix_restart'] = \
                                        int(m.groupdict()['nbr_af_maximum_prefix_restart'])
                                continue

                            #   maximum-prefix <nbr_af_maximum_prefix_max_prefix_no> [ <nbr_af_maximum_prefix_threshold> ] [ warning-only ]
                            m = p61.match(line)
                            if m:
                                bgp_vrf_af_dict['nbr_af_maximum_prefix_max_prefix_no'] = \
                                    int(m.groupdict()['nbr_af_maximum_prefix_max_prefix_no'])
                                bgp_vrf_af_dict['nbr_af_maximum_prefix_threshold'] = \
                                    int(m.groupdict()['nbr_af_maximum_prefix_threshold'])
                                if m.groupdict()['nbr_af_maximum_prefix_warning_only']:
                                    bgp_vrf_af_dict['nbr_af_maximum_prefix_warning_only'] = True
                                else:
                                    bgp_vrf_af_dict['nbr_af_maximum_prefix_warning_only'] = False
                                continue

                            #   route-map <nbr_af_route_map_name_in> in
                            m = p62.match(line)
                            if m:
                                if 'no' in line:
                                    bgp_vrf_af_dict['no_nbr_af_route_map_name_in'] = \
                                        str(m.groupdict()['nbr_af_route_map_name_in'])
                                else:
                                    bgp_vrf_af_dict['nbr_af_route_map_name_in'] = \
                                        str(m.groupdict()['nbr_af_route_map_name_in'])
                                continue

                            #   route-map <nbr_af_route_map_name_out> out
                            m = p63.match(line)
                            if m:
                                if 'no' in line:
                                    bgp_vrf_af_dict['no_nbr_af_route_map_name_out'] = \
                                        str(m.groupdict()['nbr_af_route_map_name_out'])
                                else:
                                    bgp_vrf_af_dict['nbr_af_route_map_name_out'] = \
                                        str(m.groupdict()['nbr_af_route_map_name_out'])
                                continue

                            #   route-reflector-client
                            m = p64.match(line)
                            if m:
                                bgp_vrf_af_dict['nbr_af_route_reflector_client'] = True
                                continue
                            elif 'nbr_af_route_reflector_client' not in bgp_vrf_af_dict:
                                bgp_vrf_af_dict['nbr_af_route_reflector_client'] = False

                            #   send-community
                            m = p65.match(line)
                            if m:
                                bgp_vrf_af_dict['nbr_af_send_community'] = 'standard'
                                send_community_standard_match = 'True'
                                continue

                            #   send-community extended
                            m = p66.match(line)
                            if m:
                                if send_community_standard_match:
                                    bgp_vrf_af_dict['nbr_af_send_community'] = 'both'
                                else:
                                    bgp_vrf_af_dict['nbr_af_send_community'] = 'extended'
                                continue

                            # rewrite-evpn-rt-asn
                            m = p100.match(line)
                            if m:
                                bgp_vrf_af_dict['nbr_af_rewrite_evpn_rt_asn'] = True
                                continue

                            #   route-reflector-client
                            m = p67.match(line)
                            if m:
                                bgp_vrf_af_dict['nbr_af_soft_reconfiguration'] = True
                                continue
                            elif 'nbr_af_soft_reconfiguration' not in bgp_vrf_af_dict:
                                bgp_vrf_af_dict['nbr_af_soft_reconfiguration'] = False

                            #   next-hop-self
                            m = p68.match(line)
                            if m:
                                bgp_vrf_af_dict['nbr_af_next_hop_self'] = True
                                continue
                            elif 'nbr_af_next_hop_self' not in bgp_vrf_af_dict:
                                bgp_vrf_af_dict['nbr_af_next_hop_self'] = False

                            #   as-override
                            m = p69.match(line)
                            if m:
                                bgp_vrf_af_dict['nbr_af_as_override'] = True
                                continue
                            elif 'nbr_af_as_override' not in bgp_vrf_af_dict:
                                bgp_vrf_af_dict['nbr_af_as_override'] = False

                            #   default-originate [ route-map <nbr_af_default_originate_route_map> ]
                            m = p70.match(line)
                            if m:
                                bgp_vrf_af_dict['nbr_af_default_originate'] = True
                                if m.groupdict()['nbr_af_default_originate_route_map']:
                                    bgp_vrf_af_dict['nbr_af_default_originate_route_map'] = \
                                        str(m.groupdict()['nbr_af_default_originate_route_map'])
                                continue
                            elif 'nbr_af_default_originate' not in bgp_vrf_af_dict:
                                bgp_vrf_af_dict['nbr_af_default_originate'] = False

                            #   soo <nbr_af_soo>
                            m = p71.match(line)
                            if m:
                                bgp_vrf_af_dict['nbr_af_soo'] = str(m.groupdict()['nbr_af_soo'])
                                continue

                #   template peer-session PEER-SESSION
                m = p72.match(line)
                if m:
                    # Get keys
                    ps_name = str(m.groupdict()['ps_name'])
                    if 'ps_name' not in bgp_dict['bgp']:
                        bgp_dict['bgp']['instance']['default']['ps_name'] = {}
                    if ps_name not in bgp_dict['bgp']['instance']['default']['ps_name']:
                        bgp_dict['bgp']['instance']['default']['ps_name'][ps_name] = {}
                        bgp_ps_dict = bgp_dict['bgp']['instance']['default']['ps_name'][ps_name]
                    continue

                if ps_name:
                    #   bfd
                    m = p73.match(line)
                    if m:
                        # Get keys
                        bgp_ps_dict['ps_fall_over_bfd'] = True
                        continue
                    elif 'ps_fall_over_bfd' not in bgp_ps_dict:
                        bgp_ps_dict['ps_fall_over_bfd'] = False

                    #   capability suppress 4-byte-as
                    m = p74.match(line)
                    if m:
                        bgp_ps_dict['ps_suppress_four_byte_as_capability'] = True
                        continue
                    elif 'ps_suppress_four_byte_as_capability' not in bgp_ps_dict:
                        bgp_ps_dict['ps_suppress_four_byte_as_capability'] = False

                    #   description <ps_description>
                    m = p75.match(line)
                    if m:
                        # Get keys
                        bgp_ps_dict['ps_description'] = str(m.groupdict()['ps_description'])
                        continue

                    #   disable-connected-check
                    m = p76.match(line)
                    if m:
                        bgp_ps_dict['ps_disable_connected_check'] = True
                        continue
                    elif 'ps_disable_connected_check' not in bgp_ps_dict:
                        bgp_ps_dict['ps_disable_connected_check'] = False

                    #   ebgp-multihop <ps_ebgp_multihop_max_hop>
                    m = p77.match(line)
                    if m:
                        bgp_ps_dict['ps_ebgp_multihop'] = True
                        bgp_ps_dict['ps_ebgp_multihop_max_hop'] = int(m.groupdict()['ps_ebgp_multihop_max_hop'])
                        continue
                    elif 'ps_ebgp_multihop' not in bgp_ps_dict:
                        bgp_ps_dict['ps_ebgp_multihop'] = False

                    #    { local-as <ps_local_as_as_no> [ no-prepend [ replace-as [ dual-as ] ] ] }
                    m = p78.match(line)
                    if m:
                        bgp_ps_dict['ps_local_as_as_no'] = str(m.groupdict()['ps_local_as_as_no'])
                        bgp_ps_dict['ps_local_as_no_prepend'] = True
                        bgp_ps_dict['ps_local_as_replace_as'] = True
                        bgp_ps_dict['ps_local_as_dual_as'] = True
                        continue
                    elif 'ps_local_as_no_prepend' not in bgp_ps_dict:
                        bgp_ps_dict['ps_local_as_no_prepend'] = False
                        bgp_ps_dict['ps_local_as_replace_as'] = False
                        bgp_ps_dict['ps_local_as_dual_as'] = False

                    #   password <ps_password_text>
                    m = p79.match(line)
                    if m:
                        bgp_ps_dict['ps_password_text'] = str(m.groupdict()['ps_password_text'])
                        continue

                    #   { remote-as <ps_remote_as> }
                    m = p80.match(line)
                    if m:
                        bgp_ps_dict['ps_remote_as'] = int(m.groupdict()['ps_remote_as'])
                        continue

                    #   shutdown
                    m = p81.match(line)
                    if m:
                        bgp_ps_dict['ps_shutdown'] = True
                        continue
                    elif 'ps_shutdown' not in bgp_ps_dict:
                        bgp_ps_dict['ps_shutdown'] = False

                    #   timers <ps_keepalive_interval> <ps_hodltime>
                    m = p82.match(line)
                    if m:
                        bgp_ps_dict['ps_keepalive_interval'] = int(m.groupdict()['ps_keepalive_interval'])
                        bgp_ps_dict['ps_hodltime'] = int(m.groupdict()['ps_hodltime'])
                        continue

                    #   transport connection-mode <ps_transport_connection_mode>
                    m = p83.match(line)
                    if m:
                        bgp_ps_dict['ps_transport_connection_mode'] = \
                            str(m.groupdict()['ps_transport_connection_mode'])
                        continue

                    #   update-source <ps_update_source>
                    if m:
                        bgp_ps_dict['ps_update_source'] = str(m.groupdict()['ps_update_source'])
                        continue

                #   template peer-policy <pp_name>
                m = p85.match(line)
                if m:
                    # Get keys
                    pp_name = str(m.groupdict()['pp_name'])
                    if 'pp_name' not in bgp_dict['bgp']['instance']['default']:
                        bgp_dict['bgp']['instance']['default']['pp_name'] = {}
                    if pp_name not in bgp_dict['bgp']['instance']['default']['pp_name']:
                        bgp_dict['bgp']['instance']['default']['pp_name'][pp_name] = {}
                        bgp_pp_dict = bgp_dict['bgp']['instance']['default']['pp_name'][pp_name]
                    continue

                if pp_name:
                    #   allowas-in [ <allowas-in-cnt> ]
                    m = p86.match(line)
                    if m:
                        bgp_pp_dict['pp_allowas_in'] = True
                        if m.groupdict()['pp_allowas_in_as_number']:
                            bgp_pp_dict['pp_allowas_in_as_number'] = \
                                int(m.groupdict()['pp_allowas_in_as_number'])
                        continue
                    elif 'pp_allowas_in' not in bgp_pp_dict:
                        bgp_pp_dict['pp_allowas_in'] = False

                    #   as-override
                    m = p87.match(line)
                    if m:
                        bgp_pp_dict['pp_as_override'] = True
                        continue
                    elif 'pp_as_override' not in bgp_pp_dict:
                        bgp_pp_dict['pp_as_override'] = False

                    #   default-originate [ route-map <pp_default_originate_route_map> ]
                    m = p88.match(line)
                    if m:
                        bgp_pp_dict['pp_default_originate'] = True
                        if m.groupdict()['pp_default_originate_route_map']:
                            bgp_pp_dict['pp_default_originate_route_map'] = \
                                str(m.groupdict()['pp_default_originate_route_map'])
                        continue
                    elif 'pp_default_originate' not in bgp_pp_dict:
                        bgp_pp_dict['pp_default_originate'] = False

                    #   route-map <pp_route_map_name_in> in
                    m = p89.match(line)
                    if m:
                        bgp_pp_dict['pp_route_map_name_in'] = \
                            str(m.groupdict()['pp_route_map_name_in'])
                        continue

                    #   route-map <nbr_af_route_map_name_out> out
                    m = p90.match(line)
                    if m:
                        bgp_pp_dict['pp_route_map_name_out'] = \
                            str(m.groupdict()['pp_route_map_name_out'])
                        continue

                    #    maximum-prefix <pp_maximum_prefix_max_prefix_no> [ <pp_maximum_prefix_threshold> ] [ restart <pp_maximum_prefix_restart> ]
                    m = p91.match(line)
                    if m:
                        bgp_pp_dict['pp_maximum_prefix_max_prefix_no'] = \
                            int(m.groupdict()['pp_maximum_prefix_max_prefix_no'])
                        bgp_pp_dict['pp_maximum_prefix_threshold'] = \
                            int(m.groupdict()['pp_maximum_prefix_threshold'])
                        bgp_pp_dict['pp_maximum_prefix_restart'] = \
                            int(m.groupdict()['pp_maximum_prefix_restart'])
                        continue

                    #   maximum-prefix <pp_maximum_prefix_max_prefix_no> [ <pp_maximum_prefix_threshold> ] [ warning-only ]
                    m = p92.match(line)
                    if m:
                        bgp_pp_dict['pp_maximum_prefix_max_prefix_no'] = \
                            int(m.groupdict()['pp_maximum_prefix_max_prefix_no'])

                        if m.groupdict()['pp_maximum_prefix_threshold']:
                            bgp_pp_dict['pp_maximum_prefix_threshold'] = \
                                int(m.groupdict()['pp_maximum_prefix_threshold'])

                        if m.groupdict()['pp_maximum_prefix_warning_only']:
                            bgp_pp_dict['pp_maximum_prefix_warning_only'] = True
                        else:
                            bgp_pp_dict['pp_maximum_prefix_warning_only'] = False
                        continue

                    #   next-hop-self
                    m = p93.match(line)
                    if m:
                        bgp_pp_dict['pp_next_hop_self'] = True
                        continue
                    elif 'pp_next_hop_self' not in bgp_pp_dict:
                        bgp_pp_dict['pp_next_hop_self'] = False

                    #   route-reflector-client
                    m = p94.match(line)
                    if m:
                        bgp_pp_dict['pp_route_reflector_client'] = True
                        continue
                    elif 'pp_route_reflector_client' not in bgp_pp_dict:
                        bgp_pp_dict['pp_route_reflector_client'] = False

                    #   send-community
                    m = p95.match(line)
                    if m:
                        bgp_pp_dict['pp_send_community'] = 'standard'
                        peer_policy_send_community_standard_match = 'True'
                        continue

                    #   send-community extended
                    m = p96.match(line)
                    if m:
                        if peer_policy_send_community_standard_match:
                            bgp_pp_dict['pp_send_community'] = 'both'
                        else:
                            bgp_pp_dict['pp_send_community'] = 'extended'
                        continue

                    #   route-reflector-client
                    m = p97.match(line)
                    if m:
                        bgp_pp_dict['pp_soft_reconfiguration'] = True
                        continue
                    elif 'pp_soft_reconfiguration' not in bgp_pp_dict:
                        bgp_pp_dict['pp_soft_reconfiguration'] = False

                    #   soo <pp_soo>
                    m = p98.match(line)
                    if m:
                        bgp_pp_dict['pp_soo'] = str(m.groupdict()['pp_soo'])
                        continue

                # template peer PEER
                m = peer_1.match(line)
                if m:
                    peer_name = m.groupdict()['peer_name']
                    if 'peer_name' not in bgp_dict['bgp']['instance']['default']:
                        bgp_dict['bgp']['instance']['default']['peer_name'] = {}
                    if peer_name not in bgp_dict['bgp']['instance']['default']['peer_name']:
                        bgp_dict['bgp']['instance']['default']['peer_name'][peer_name] = {}
                        bgp_peer_dict = bgp_dict['bgp']['instance']['default']['peer_name'][peer_name]
                    continue

                if peer_name != '':
                    #   bfd
                    m = p73.match(line)
                    if m:
                        # Get keys
                        bgp_peer_dict['peer_fall_over_bfd'] = True
                        continue
                    elif 'peer_fall_over_bfd' not in bgp_peer_dict:
                        bgp_peer_dict['peer_fall_over_bfd'] = False
                        continue

                    #   { remote-as <remote_as> }
                    m = p80.match(line)
                    if m:
                        bgp_peer_dict['peer_remote_as'] = int(m.groupdict()['ps_remote_as'])
                        continue

                    #   password <password_text>
                    m = p79.match(line)
                    if m:
                        bgp_peer_dict['peer_password_text'] = str(m.groupdict()['ps_password_text'])
                        continue

                    #   address-family <af_name>
                    m = p57.match(line)
                    if m:
                        peer_af_name = str(m.groupdict()['nbr_af_name'])
                        if 'peer_af_name' not in bgp_peer_dict:
                            bgp_peer_dict['peer_af_name'] = {}
                        if peer_af_name not in bgp_peer_dict['peer_af_name']:
                            bgp_peer_dict['peer_af_name'][peer_af_name] = {}
                            bgp_peer_af_dict = bgp_peer_dict['peer_af_name'][peer_af_name]
                        continue

                    if 'peer_af_name' in bgp_peer_dict:

                        #   send-community
                        m = p65.match(line)
                        if m:
                            bgp_peer_af_dict['peer_af_send_community'] = 'standard'
                            send_community_standard_match = 'True'
                            continue

                        #   maximum-prefix <pp_maximum_prefix_max_prefix_no> [ <pp_maximum_prefix_threshold> ] [ warning-only ]
                        m = p92.match(line)
                        if m:
                            bgp_peer_af_dict['peer_maximum_prefix_max_prefix_no'] = \
                                int(m.groupdict()['pp_maximum_prefix_max_prefix_no'])

                            if m.groupdict()['pp_maximum_prefix_threshold']:
                                bgp_peer_af_dict['peer_maximum_prefix_threshold'] = \
                                    int(m.groupdict()['pp_maximum_prefix_threshold'])

                            if m.groupdict()['pp_maximum_prefix_warning_only']:
                                bgp_peer_af_dict['peer_maximum_prefix_warning_only'] = True
                            else:
                                bgp_peer_af_dict['peer_maximum_prefix_warning_only'] = False
                            continue

                        #   next-hop-self
                        m = p68.match(line)
                        if m:
                            bgp_peer_af_dict['peer_next_hop_self'] = True
                            continue
                        elif 'peer_next_hop_self' not in bgp_peer_af_dict:
                            bgp_peer_af_dict['peer_next_hop_self'] = False
                            continue

        return bgp_dict


# ===================================================
# Schema for 'show bgp all dampening flap-statistics'
# ===================================================
class ShowBgpAllDampeningFlapStatisticsSchema(MetaParser):
    """Schema for show bgp all dampening flap-statistics"""

    schema = {
        'vrf': {
            Any(): {
                'address_family': {
                    Any(): {
                        Optional('network'): {
                            Any(): {
                                'peer': str,
                                'flaps': int,
                                'duration': str,
                                'current_penalty': int,
                                'suppress_limit': int,
                                'reuse_limit': int,
                                'best': bool,
                                Optional('status'): str,
                                Optional('reuse_time'): str,
                                Optional('pathtype'): str,
                            },
                        },
                        Optional('history_paths'): int,
                        Optional('dampened_paths'): int,
                        Optional('dampening_enabled'): bool,
                        Optional('route_identifier'): {
                            Any(): {
                                Optional('network'): {
                                    Any(): {
                                        'peer': str,
                                        'flaps': int,
                                        'duration': str,
                                        Optional('reuse_time'): str,
                                        'current_penalty': int,
                                        'suppress_limit': int,
                                        'reuse_limit': int,
                                        'best': bool,
                                        Optional('status'): str,
                                        Optional('pathtype'): str,
                                    },
                                },
                                'history_paths': int,
                                'dampened_paths': int,
                                'dampening_enabled': bool,
                            },
                        }
                    },                            
                },
            },
        }
    }

# ===================================================
# Parser for 'show bgp all dampening flap-statistics'
# ===================================================
class ShowBgpAllDampeningFlapStatistics(ShowBgpAllDampeningFlapStatisticsSchema):
    """Parser for:
        show bgp all dampening flap-statistics
        parser class implements detail parsing mechanisms for cli,xml output."""

    cli_command = 'show bgp all dampening flap-statistics'
    xml_command = 'show bgp all dampening flap-statistics | xml'
    exclude = ['duration']

    def cli(self,output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        # Init vars
        ret_dict = {}
        sub_dict = {}
        history_paths = None
        dampened_paths = None
        p1 = re.compile(r'^Flap +Statistics +for +VRF +'
                            r'(?P<vrf_name>[\w\-]+), +address +family +'
                            r'(?P<address_family>[\w\s\-]+):$')
        p2 = re.compile(r'^Dampening +configured, +'
                            r'(?P<history_paths>\d+) +history +paths, +'
                            r'(?P<dampened_paths>\d+) +dampened +paths$')
        p2_1 = re.compile(r'^Dampening +not +configured, +'
                            r'(?P<history_paths>\d+) +history +paths, +'
                            r'(?P<dampened_paths>\d+) +dampened +paths$')
        p3 = re.compile(r'^Route +Distinguisher: +'
                            r'(?P<route_identifier>[\w\.\:]+)$')
        p4 = re.compile(r'^(?P<status>[\*|d|s|h|\s])?'
                            r'(?P<best>[\>|\s])?'
                            r'(?P<pathtype>[e|i])?'
                            r' +(?P<network>\S+)'
                            r' +(?P<peer>[\w\/\.\:]+)'
                            r' +(?P<flaps>\d+)'
                            r' +(?P<duration>[\w\:\.]+)'
                            r'(?: +(?P<reuse_time>[\w\:\.]+))?'
                            r' +(?P<current_penalty>\d+)\/'
                            r'(?P<suppress_limit>\d+)\/(?P<reuse_limit>\d+)$')
        p4_1 = re.compile(r'^(?P<status>[\*|d|s|h|\s])?'
                            r'(?P<best>[\>|\s])?'
                            r'(?P<pathtype>[e|i|\s])?'
                            r' +(?P<network>\S+\/\d{1,3})'
                            r'(?P<peer>[1|2][\d\.\:]+)'
                            r' +(?P<flaps>\d+)'
                            r' +(?P<duration>[\w\:\.]+)'
                            r'(?: +(?P<reuse_time>[\w\:\.]+))?'
                            r' +(?P<current_penalty>\d+)\/'
                            r'(?P<suppress_limit>\d+)\/(?P<reuse_limit>\d+)$')

        for line in out.splitlines():
            line = line.strip()

            # build keys for dampened_paths and history_paths
            if isinstance(dampened_paths, int):
                sub_dict['dampened_paths'] = dampened_paths
                sub_dict.setdefault('dampening_enabled', dampening_enabled) \
                    if dampening_enabled else None
                
            if isinstance(history_paths, int):
                sub_dict['history_paths'] = history_paths

            # Flap Statistics for VRF default, address family IPv4 Unicast:
            m = p1.match(line)
            if m:
                address_family = m.groupdict()['address_family'].lower()
                vrf = m.groupdict()['vrf_name']

                if 'vrf' not in ret_dict:
                    ret_dict['vrf'] = {}

                if vrf not in ret_dict['vrf']:
                    ret_dict['vrf'][vrf] = {}

                if 'address_family' not in ret_dict['vrf'][vrf]:
                    ret_dict['vrf'][vrf]['address_family'] = {}

                if address_family not in ret_dict['vrf'][vrf]['address_family']:
                    ret_dict['vrf'][vrf]['address_family'][address_family] = {}
                    sub_dict = ret_dict['vrf'][vrf]['address_family'][address_family]
                        
                # reset variable
                dampened_paths = None
                history_paths = None
                continue

            # Dampening configured, 0 history paths, 2 dampened paths
            m = p2.match(line)
            if m:
                history_paths = int(m.groupdict()['history_paths'])
                dampened_paths = int(m.groupdict()['dampened_paths'])
                dampening_enabled = True
                continue

            # Dampening not configured, 0 history paths, 0 dampened paths
            m = p2_1.match(line)
            if m:
                history_paths = int(m.groupdict()['history_paths'])
                dampened_paths = int(m.groupdict()['dampened_paths'])
                dampening_enabled = False
                continue

            # Route Distinguisher: 0:0
            m = p3.match(line)
            if m:
                route_identifier = m.groupdict()['route_identifier']
                if 'route_identifier' not in ret_dict['vrf'][vrf]\
                    ['address_family'][address_family]:
                    ret_dict['vrf'][vrf]['address_family'][address_family]\
                        ['route_identifier'] = {}

                if route_identifier not in ret_dict['vrf'][vrf]\
                    ['address_family'][address_family]['route_identifier']:
                    ret_dict['vrf'][vrf]['address_family'][address_family]\
                        ['route_identifier'][route_identifier] = {}

                    sub_dict = ret_dict['vrf'][vrf]['address_family'][address_family]\
                        ['route_identifier'][route_identifier]
                continue

            # d e 10.25.1.0/24       10.106.102.3                38   00:09:36 00:01:40  35/30/10
            # *>e 10.4.0.0/24       192.168.64.1                 1   00:20:56          570/1500/1000
            m = p4.match(line)

            # d e [2]:[77][7,0][10.219.39.39,2,656877351][10.70.1.1,22][10.106.102.3,10.246.1.31]/61610.106.102.3                38   00:09:36 00:01:40 34/30/10
            m1 = p4_1.match(line)
            m = m if m else m1
            if m:
                network = m.groupdict()['network']
                if 'network' not in sub_dict:
                    sub_dict['network'] = {}
                if network not in sub_dict['network']:
                    sub_dict['network'][network] = {}

                if not m.groupdict()['best'].isspace():
                    sub_dict['network'][network]['best'] = True
                else:
                    sub_dict['network'][network]['best'] = False
                sub_dict['network'][network]['status'] = m.groupdict()['status']
                sub_dict['network'][network]['pathtype'] = m.groupdict()['pathtype']
                sub_dict['network'][network]['peer'] = m.groupdict()['peer']
                sub_dict['network'][network]['flaps'] = int(m.groupdict()['flaps'])
                sub_dict['network'][network]['duration'] = m.groupdict()['duration']
                if m.groupdict()['reuse_time']:
                    sub_dict['network'][network]['reuse_time'] = m.groupdict()['reuse_time']
                sub_dict['network'][network]['current_penalty'] = \
                    int(m.groupdict()['current_penalty'])
                sub_dict['network'][network]['suppress_limit'] = \
                    int(m.groupdict()['suppress_limit'])
                sub_dict['network'][network]['reuse_limit'] = \
                    int(m.groupdict()['reuse_limit'])
                continue
        return ret_dict


    def xml(self):
        out = self.device.execute(self.xml_command)

        etree_dict = {}
        sub_dict = {}
        # Remove junk characters returned by the device
        out = out.replace("]]>]]>", "")
        root = ET.fromstring(out)

        # top table root
        show_root = Common.retrieve_xml_child(root=root, key='show')
        # get xml namespace
        # {http://www.cisco.com/nxos:7.0.3.I7.1.:bgp}
        try:
            m = re.compile(r'(?P<name>\{[\S]+\})').match(show_root.tag)
            namespace = m.groupdict()['name']
        except Exception:
            return etree_dict

        # compare cli command
        Common.compose_compare_command(root=root, namespace=namespace,
                                expect_command=self.cli_command)

        # top table root
        vrf_root = Common.retrieve_xml_child(root=root, key='TABLE_vrf')
        if not vrf_root:
            return etree_dict

        # -----   loop vrf  -----
        for vrf_tree in vrf_root.findall('{}ROW_vrf'.format(namespace)):
            # vrf
            try:
                vrf = vrf_tree.find('{}vrf-name-out'.format(namespace)).text
            except Exception:
                break

            # address_family table
            afi = vrf_tree.find('{}TABLE_afi'.format(namespace))

            # -----   loop address_family  -----
            for af_root in afi.findall('{}ROW_afi'.format(namespace)):

                # address_family
                row_safi = af_root.find('{}TABLE_safi'.format(namespace))
                row_safi = row_safi.find('{}ROW_safi'.format(namespace))

                try:
                    af = row_safi.find('{}af-name'.format(namespace)).text.lower()
                except Exception:
                    continue

                # rd table
                rd = row_safi.find('{}TABLE_rd'.format(namespace))
                if not rd:
                    continue
                else:
                    if 'vrf' not in etree_dict:
                        etree_dict['vrf'] = {}
                    if vrf not in etree_dict['vrf']:
                        etree_dict['vrf'][vrf] = {}

                    if 'address_family' not in etree_dict['vrf'][vrf]:
                        etree_dict['vrf'][vrf]['address_family'] = {}
                    if af not in etree_dict['vrf'][vrf]['address_family']:
                        etree_dict['vrf'][vrf]['address_family'][af] = {}

                # -----   loop rd  -----
                for rd_root in rd.findall('{}ROW_rd'.format(namespace)):
                    # rd
                    try:
                        rd = rd_root.find('{}rd_val'.format(namespace)).text
                    except Exception:
                        rd = None

                    # <dampeningenabled>true</dampeningenabled>
                    try:
                        dampeningenabled = rd_root.find('{}dampeningenabled'
                                                        .format(namespace)).text
                    except Exception:
                        # <dampening>true</dampening>
                        try:
                            dampeningenabled = rd_root.find('{}dampening'
                                                            .format(namespace)).text
                        except Exception:
                            pass
                            
                    # <historypaths>0</historypaths>
                    historypaths = int(rd_root.find('{}historypaths'
                                                    .format(namespace)).text)
                    # <dampenedpaths>2</dampenedpaths>
                    dampenedpaths = int(rd_root.find('{}dampenedpaths'
                                                     .format(namespace)).text)

                    if rd:
                        # set default attributes under address family 
                        # <dampeningenabled>true</dampeningenabled>
                        if dampeningenabled == 'true':
                            etree_dict['vrf'][vrf]['address_family'][af]['dampening_enabled'] = True

                        # <historypaths>0</historypaths>
                        etree_dict['vrf'][vrf]['address_family'][af]['history_paths'] = historypaths
                        
                        # <dampenedpaths>2</dampenedpaths>
                        etree_dict['vrf'][vrf]['address_family'][af]['dampened_paths'] = dampenedpaths

                        if 'route_identifier' not in etree_dict['vrf'][vrf]\
                            ['address_family'][af]:
                            etree_dict['vrf'][vrf]['address_family'][af]\
                                ['route_identifier'] = {}

                        if rd not in etree_dict['vrf'][vrf]\
                            ['address_family'][af]['route_identifier']:
                            etree_dict['vrf'][vrf]['address_family'][af]\
                                ['route_identifier'][rd] = {}

                        sub_dict = etree_dict['vrf'][vrf]['address_family'][af]\
                            ['route_identifier'][rd]
                    else:
                        sub_dict = etree_dict['vrf'][vrf]['address_family'][af]

                    # <dampeningenabled>true</dampeningenabled>
                    if dampeningenabled == 'true':
                        sub_dict['dampening_enabled'] = True

                    # <historypaths>0</historypaths>
                    sub_dict['history_paths'] = historypaths

                    # <dampenedpaths>2</dampenedpaths>
                    sub_dict['dampened_paths'] = dampenedpaths

                    # prefix table
                    prefix = rd_root.find('{}TABLE_prefix'.format(namespace))
                    if not prefix:
                        continue

                    # -----   loop prefix  -----
                    for prefix_root in prefix.findall('{}ROW_prefix'.format(namespace)):

                        # <ipprefix>10.25.1.0/24</ipprefix>
                        try:
                            network = prefix_root.find('{}ipprefix'.format(namespace)).text
                        except Exception:
                            pass

                        # ipv6prefix>2001::/112</ipv6prefix>
                        try:
                            network = prefix_root.find('{}ipv6prefix'.format(namespace)).text
                        except Exception:
                            pass

                        # <nonipprefix>[2]:[0]:[0]:[48]:[0201.02ff.0302]:[32]:[10.81.1.1]/248</nonipprefix>
                        try:
                            network = prefix_root.find('{}nonipprefix'.format(namespace)).text
                        except Exception:
                            pass
                           
                        if 'network' not in sub_dict:
                            sub_dict['network'] = {}

                        if network not in sub_dict['network']:
                            sub_dict['network'][network] = {}

                        # <status>d</status>
                        sub_dict['network'][network]['status'] = \
                            prefix_root.find('{}status'.format(namespace)).text

                        # <pathtype>e</pathtype>
                        sub_dict['network'][network]['pathtype'] = \
                            prefix_root.find('{}pathtype'.format(namespace)).text

                        # <peer>10.106.102.3</peer>
                        try:
                            sub_dict['network'][network]['peer'] = \
                                prefix_root.find('{}peer'.format(namespace)).text
                        except Exception:
                            pass

                        # <ipv6peer>2001:db8:8d82::2002</ipv6peer>
                        try:
                            sub_dict['network'][network]['peer'] = \
                                prefix_root.find('{}ipv6peer'.format(namespace)).text
                        except Exception:
                            pass

                        # <flapcount>39</flapcount>
                        sub_dict['network'][network]['flaps'] = \
                            int(prefix_root.find('{}flapcount'.format(namespace)).text)
                            
                        # <duration>00:09:53</duration>
                        sub_dict['network'][network]['duration'] = \
                            prefix_root.find('{}duration'.format(namespace)).text
                            
                        # <reuse>00:01:40</reuse>
                        reuse = prefix_root.find('{}reuse'.format(namespace)).text
                        if reuse:
                            sub_dict['network'][network]['reuse_time'] = reuse
                            
                            
                        # <penalty>34</penalty>
                        penalty = prefix_root.find('{}penalty'.format(namespace)).text
                        if penalty:
                            sub_dict['network'][network]['current_penalty'] = int(penalty)
                            
                        # <suppresslimit>30</suppresslimit>
                        sub_dict['network'][network]['suppress_limit'] = \
                            int(prefix_root.find('{}suppresslimit'.format(namespace)).text)

                       # <reuselimit>10</reuselimit>
                        sub_dict['network'][network]['reuse_limit'] = \
                            int(prefix_root.find('{}reuselimit'.format(namespace)).text)

                       # <best>false</best>
                        if prefix_root.find('{}best'.format(namespace)).text == 'false':
                            sub_dict['network'][network]['best'] = False
                        else:
                            sub_dict['network'][network]['best'] = True                                                                                    
        return etree_dict


# ==========================================
# Parser for 'show bgp all nexthop-database'
# ==========================================
class ShowBgpAllNexthopDatabase(ShowBgpVrfAllAllNextHopDatabase):
    """Parser for:
        show bgp all nexthop-database
        parser class implements detail parsing mechanisms for cli,xml output."""

    cli_command = 'show bgp all nexthop-database'
    xml_command = 'show bgp all nexthop-database | xml'
    exclude = [
    'resolve_time',
    'rnh_epoch',
    'flags',
    'metric_next_advertise',
    'refcount',
    'igp_cost',
    'igp_preference',
    'current_penalty']

    def cli(self,output=None):
        return super().cli(cmd=self.cli_command,output=output)

    def xml(self):
        out = self.device.execute(self.xml_command)

        etree_dict = {}
        sub_dict = {}
        # Remove junk characters returned by the device
        out = out.replace("]]>]]>", "")
        root = ET.fromstring(out)

        # top table root
        show_root = Common.retrieve_xml_child(root=root, key='show')
        # get xml namespace
        # {http://www.cisco.com/nxos:7.0.3.I7.1.:bgp}
        try:
            m = re.compile(r'(?P<name>\{[\S]+\})').match(show_root.tag)
            namespace = m.groupdict()['name']
        except Exception:
            return etree_dict

        # compare cli command
        Common.compose_compare_command(root=root, namespace=namespace,
                                expect_command=self.cli_command)

        # top table root
        vrf_root = Common.retrieve_xml_child(root=root, key='TABLE_nhvrf')
        if not vrf_root:
            return etree_dict

        # -----   loop vrf  -----
        for vrf_tree in vrf_root.findall('{}ROW_nhvrf'.format(namespace)):
            # vrf
            try:
                vrf = vrf_tree.find('{}nhvrf-name-out'.format(namespace)).text
            except Exception:
                break

            if 'vrf' not in etree_dict:
                etree_dict['vrf'] = {}
            if vrf not in etree_dict['vrf']:
                etree_dict['vrf'][vrf] = {}

            # address_family table
            afi = vrf_tree.find('{}TABLE_nhafi'.format(namespace))

            # -----   loop address_family  -----
            for af_root in afi.findall('{}ROW_nhafi'.format(namespace)):

                # address_family
                row_safi = af_root.find('{}TABLE_nhsafi'.format(namespace))
                af_root = row_safi.find('{}ROW_nhsafi'.format(namespace))
                try:
                    af = af_root.find('{}af-name'.format(namespace)).text.lower()
                except Exception:
                    continue

                if 'address_family' not in etree_dict['vrf'][vrf]:
                    etree_dict['vrf'][vrf]['address_family'] = {}
                if af not in etree_dict['vrf'][vrf]['address_family']:
                    etree_dict['vrf'][vrf]['address_family'][af] = {}

                # af_nexthop_trigger_enable
                etree_dict['vrf'][vrf]['address_family'][af]\
                    ['af_nexthop_trigger_enable'] = True

                # <nhnoncriticaldelay>10000</nhnoncriticaldelay>
                etree_dict['vrf'][vrf]['address_family'][af]\
                    ['nexthop_trigger_delay_non_critical'] = int(af_root.find('{}nhnoncriticaldelay'
                                                             .format(namespace)).text)
                # <nhcriticaldelay>3000</nhcriticaldelay>
                etree_dict['vrf'][vrf]['address_family'][af]\
                    ['nexthop_trigger_delay_critical'] = int(af_root.find('{}nhcriticaldelay'
                                                             .format(namespace)).text)

                # nexthop table
                next_hop = af_root.find('{}TABLE_nexthop'.format(namespace))
                if not next_hop:
                    continue

                # -----   loop nexthop  -----
                for nexthop_root in next_hop.findall('{}ROW_nexthop'.format(namespace)):
                    # nexthop
                    # <ipnexthop-out>192.168.154.1</ipnexthop-out>
                    try:
                        nexthop = nexthop_root.find('{}ipnexthop-out'.format(namespace)).text
                    except Exception:
                        pass

                    # <ipv6nexthop-out>2001:db8:400::3:1</ipv6nexthop-out>
                    try:
                        nexthop = nexthop_root.find('{}ipv6nexthop-out'.format(namespace)).text
                    except Exception:
                        pass

                    if 'next_hop' not in etree_dict['vrf'][vrf]\
                        ['address_family'][af]:
                        etree_dict['vrf'][vrf]['address_family'][af]\
                            ['next_hop'] = {}

                    if nexthop not in etree_dict['vrf'][vrf]\
                        ['address_family'][af]['next_hop']:
                        etree_dict['vrf'][vrf]['address_family'][af]\
                            ['next_hop'][nexthop] = {}

                    sub_dict = etree_dict['vrf'][vrf]['address_family'][af]\
                        ['next_hop'][nexthop]

                    # <refcount>1</refcount>
                    sub_dict['refcount'] = int(nexthop_root.find(
                                                '{}refcount'.format(namespace)).text)

                    # <igpmetric>3</igpmetric>
                    sub_dict['igp_cost'] = \
                        int(nexthop_root.find('{}igpmetric'.format(namespace)).text)

                    # <multipath>false</multipath>
                    try:
                        if nexthop_root.find('{}multipath'.format(namespace)).text == 'false':
                            sub_dict['multipath'] = 'No'
                        else:
                            sub_dict['multipath'] = 'Yes'
                    except Exception:
                        pass

                    # <igptype>0</igptype>
                    sub_dict['igp_route_type'] = \
                        int(nexthop_root.find('{}igptype'.format(namespace)).text)

                    # <igppref>110</igppref>
                    sub_dict['igp_preference'] = \
                        int(nexthop_root.find('{}igppref'.format(namespace)).text)

                    # <attached>false</attached>
                    if nexthop_root.find('{}attached'.format(namespace)).text == 'false':
                        sub_dict['attached'] = False
                    else:
                        sub_dict['attached'] = True


                    # <local>false</local>
                    if nexthop_root.find('{}local'.format(namespace)).text == 'false':
                        sub_dict['local'] = False
                    else:
                        sub_dict['local'] = True

                    # <reachable>true</reachable>
                    if nexthop_root.find('{}reachable'.format(namespace)).text == 'false':
                        sub_dict['reachable'] = False
                    else:
                        sub_dict['reachable'] = True

                    # <labeled>true</labeled>
                    if nexthop_root.find('{}labeled'.format(namespace)).text == 'false':
                        sub_dict['labeled'] = False
                    else:
                        sub_dict['labeled'] = True

                    # <filtered>false</filtered>
                    if nexthop_root.find('{}filtered'.format(namespace)).text == 'false':
                        sub_dict['filtered'] = False
                    else:
                        sub_dict['filtered'] = True

                    # <pendingupdate>false</pendingupdate>
                    if nexthop_root.find('{}pendingupdate'.format(namespace)).text == 'false':
                        sub_dict['pending_update'] = False
                    else:
                        sub_dict['pending_update'] = True

                    # <resolvetime>18:38:21</resolvetime>
                    sub_dict['resolve_time'] = \
                        nexthop_root.find('{}resolvetime'.format(namespace)).text

                    # <ribroute>192.168.154.1/32</ribroute>
                    try:
                        sub_dict['rib_route'] = \
                            nexthop_root.find('{}ribroute'.format(namespace)).text
                    except Exception:
                        pass                    

                    # <ipv6ribroute>0::/0</ipv6ribroute>
                    try:
                        sub_dict['rib_route'] = \
                            nexthop_root.find('{}ipv6ribroute'.format(namespace)).text
                    except Exception:
                        pass

                    # <nextadvertise>Never</nextadvertise>
                    sub_dict['metric_next_advertise'] = \
                        nexthop_root.find('{}nextadvertise'.format(namespace)).text.lower()

                    # <rnhepoch>1</rnhepoch>
                    sub_dict['rnh_epoch'] = \
                        int(nexthop_root.find('{}rnhepoch'.format(namespace)).text)


                    # attachedhops table
                    attached = nexthop_root.find('{}TABLE_attachedhops'.format(namespace))
                    if not attached:
                        continue

                    # -----   loop attachedhops  -----
                    for attach_root in attached.findall('{}ROW_attachedhops'.format(namespace)):

                        # <attachedhop>192.168.66.2</attachedhop>
                        try:
                            att_hop = attach_root.find('{}attachedhop'.format(namespace)).text
                        except Exception:
                            pass

                        # <ipv6attachedhop>fe80::6e9c:edff:fe4d:ff41</ipv6attachedhop>
                        try:
                            att_hop = attach_root.find('{}ipv6attachedhop'.format(namespace)).text
                        except Exception:
                            pass
                           
                        if 'attached_nexthop' not in sub_dict:
                            sub_dict['attached_nexthop'] = {}

                        if att_hop not in sub_dict['attached_nexthop']:
                            sub_dict['attached_nexthop'][att_hop] = {}

                        # <interface>port-channel2.100</interface>
                        sub_dict['attached_nexthop'][att_hop]['attached_nexthop_interface'] = \
                            attach_root.find('{}interface'.format(namespace)).text                                                                                                          
        return etree_dict


# ===================================
# Schema for 'show bgp peer-template'
# ===================================
class ShowBgpPeerTemplateCmdSchema(MetaParser):
    """Schema for show bgp peer-template"""

    schema = {
        'template': {
            Any(): {
                Optional('source_interface'): str,
                Optional('low_mem_exempt'): bool,
                Optional('logging_neighbor_events'): bool,
                Optional('external_bgp_peer_hops_limit'): int,
                Optional('passive_only'): bool,
                Optional('local_as_inactive'): bool,
                Optional('remove_private_as'): bool,
                Optional('vrf'): {
                    Any(): {
                        'inheriting_peer': {
                            Any(): {
                                'inheriting_peer': str,
                            },
                        }
                    },
                },
                'address_family': {
                    Any(): {
                        Optional('condition_map'): str,
                        Optional('advertise_map'): str,
                        Optional('advertise_map_status'): str,
                        Optional('in_soft_reconfig_allowed'): bool,
                        Optional('send_community'): bool,
                        Optional('send_ext_community'): bool,
                        Optional('local_nexthop'): str,
                        Optional('third_party_nexthop'): bool,
                        Optional('max_pfx'): int,
                        Optional('soo'): str,
                        Optional('weight'): int,
                        Optional('allow_as_in'): int,
                        Optional('as_override'): bool,
                        Optional('peer_as_check_disabled'): bool,
                        Optional('rr_configured'): bool,
                        Optional('default_originate'): bool,
                        Optional('default_originate_route_map'): str,
                        Optional('unsuppress_map'): str,
                        Optional('in_policy'): {
                            Any(): {
                                'type': str,
                                'name': str,
                            },
                        },
                        Optional('out_policy'): {
                            Any(): {
                                'type': str,
                                'name': str,
                            },
                        },                        
                    },                            
                },
            },
        }
    }

# ===================================
# Parser for 'show bgp peer-template'
# ===================================
class ShowBgpPeerTemplateCmd(ShowBgpPeerTemplateCmdSchema):
    """Parser for:
        show bgp peer-template
    parser class implements detail parsing mechanisms for cli,xml output."""

    cli_command = 'show bgp peer-template'
    xml_command = 'show bgp peer-template | xml'

    def cli(self,output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        # Init vars
        ret_dict = {}
        sub_dict = {}
        tem_peer = None

        p1 = re.compile(r'^BGP +peer\-template +is +'
                            r'(?P<template>[\w\-]+)$')
        p2 = re.compile(r'^Using +(?P<intf>[\w\-\/\.]+) +as'
                            r' +update +source +for +this +peer$')
        p3 = re.compile(r'^Peer +is +low\-memory +exempt$')
        p4 = re.compile(r'^Disable +logging +neighbor +events$')
        p5 = re.compile(r'^External +BGP +peer +might +be +up +to'
                            r' +(?P<hops>\d+) +hops +away$')
        p6 = re.compile(r'^Only +passive +connection +setup +allowed$')
        p23 = re.compile(r'^Neighbor +local\-as +command +not +active$')
        p7 = re.compile(r'^For +address +family: +(?P<af>[\w\s\-]+)$')
        p8 = re.compile(r'^Condition\-map +(?P<con_map>[\w\-]+), +'
                            r'Advertise\-map +(?P<adv_map>[\w\-]+), +'
                            r'Status +(?P<status>[\w\-]+)$')
        p25 = re.compile(r'^Inbound +soft +reconfiguration +allowed(?: *\(always\))?$')
        p9 = re.compile(r'^Community +attribute +sent +to +this +neighbor$')
        p10 = re.compile(r'^Extended +community +attribute +sent +'
                            r'to +this +neighbor$')
        p11 = re.compile(r'^Nexthop(?: +always)? +set +to +local +'
                            r'peering +address, +(?P<local_nexthop>[\w\.\:]+)$')
        p12 = re.compile(r'^Third\-party +Nexthop +will +not +be +computed.$')
        p13 = re.compile(r'^Maximum +prefixes +allowed +(?P<max_pfx>\d+)$')
        p14 = re.compile(r'^SOO +Extcommunity: +(?P<soo>[\w\:\.]+)$')
        p15 = re.compile(r'^Weight: +(?P<weight>\d+)$')
        p16 = re.compile(r'^Allow +my +ASN +(?P<asn>\d+) +times$')
        p17 = re.compile(r'^ASN +override +is +(?P<status>\w+)$')
        p24 = re.compile(r'^Peer +ASN +check +is +disabled$')
        p18 = re.compile(r'^Inbound +(?P<type>[\w\-\s]+) +configured'
                            r' +is +(?P<name>[\w\-]+)$')
        p19 = re.compile(r'^Outbound +(?P<type>[\w\-\s]+) +configured'
                            r' +is +(?P<name>[\w\-]+)$')
        p20 = re.compile(r'^Default +information +originate(, +'
                            r'route-map +(?P<map>[\w\-]+))? +(?P<dummy>.*)$')
        p21 = re.compile(r'^Unsuppress\-map +(?P<map>[\w\-]+) +configured$')
        p22 = re.compile(r'^Members +of +peer\-template +(?P<peer>[\w\-]+):$')
        p22_1 = re.compile(r'^(?P<vrf>[\w\-]+): +(?P<neighbor>[\w\:\.]+)$')

        for line in out.splitlines():
            line = line.strip()

            # BGP peer-template is PEER2
            m = p1.match(line)
            if m:
                template = m.groupdict()['template']

                if 'template' not in ret_dict:
                    ret_dict['template'] = {}

                if template not in ret_dict['template']:
                    ret_dict['template'][template] = {}

                # will enable regext when there is output
                # initial the flag due to comparison with xml version
                ret_dict['template'][template]['local_as_inactive'] = False
                ret_dict['template'][template]['remove_private_as'] = False
                ret_dict['template'][template]['logging_neighbor_events'] = False
                ret_dict['template'][template]['passive_only'] = False
                continue

            # Using loopback1 as update source for this peer
            m = p2.match(line)
            if m:
                ret_dict['template'][template]['source_interface'] = \
                    m.groupdict()['intf']
                continue

            # Peer is low-memory exempt
            m = p3.match(line)
            if m:
                ret_dict['template'][template]['low_mem_exempt'] = True
                continue

            # Disable logging neighbor events
            m = p4.match(line)
            if m:
                ret_dict['template'][template]['logging_neighbor_events'] = False
                continue

            # External BGP peer might be up to 100 hops away
            m = p5.match(line)
            if m:
                ret_dict['template'][template]['external_bgp_peer_hops_limit'] = \
                    int(m.groupdict()['hops'])
                continue

            # Only passive connection setup allowed
            m = p6.match(line)
            if m:
                ret_dict['template'][template]['passive_only'] = True
                continue

            # Neighbor local-as command not active
            m = p23.match(line)
            if m:
                ret_dict['template'][template]['local_as_inactive'] = True
                continue

            # For address family: IPv4 Unicast
            m = p7.match(line)
            if m:
                af = m.groupdict()['af'].lower()

                if 'address_family' not in ret_dict['template'][template]:
                    ret_dict['template'][template]['address_family'] = {}

                if af not in ret_dict['template'][template]['address_family']:
                    ret_dict['template'][template]['address_family'][af] = {}

                sub_dict = ret_dict['template'][template]['address_family'][af]

                # will enable regext when there is output
                # initial the flag due to comparison with xml version
                sub_dict['in_soft_reconfig_allowed'] = False
                sub_dict['rr_configured'] = False
                sub_dict['peer_as_check_disabled'] = False
                sub_dict['as_override'] = False
                sub_dict['default_originate'] = False
                continue

            # Condition-map DENY_ALL_RM, Advertise-map BLOCK-ALL, Status Advertise
            m = p8.match(line)
            if m:
                sub_dict['condition_map'] = m.groupdict()['con_map']
                sub_dict['advertise_map'] = m.groupdict()['adv_map']
                sub_dict['advertise_map_status'] = m.groupdict()['status'].lower()
                continue

            # Inbound soft reconfiguration allowed(always)
            m = p25.match(line)
            if m:
                sub_dict['in_soft_reconfig_allowed'] = True
                continue

            # Community attribute sent to this neighbor
            m = p9.match(line)
            if m:
                sub_dict['send_community'] = True
                continue

            # Extended community attribute sent to this neighbor
            m = p10.match(line)
            if m:
                sub_dict['send_ext_community'] = True
                continue

            # Nexthop always set to local peering address, 0.0.0.0
            # Nexthop set to local peering address, 0.0.0.0
            m = p11.match(line)
            if m:
                sub_dict['local_nexthop'] = m.groupdict()['local_nexthop']
                continue

            # Third-party Nexthop will not be computed.
            # will enhance this when output for third_party_nexthop is enabled
            m = p12.match(line)
            if m:
                sub_dict['third_party_nexthop'] = False
                continue

            # Maximum prefixes allowed 888888888
            m = p13.match(line)
            if m:
                sub_dict['max_pfx'] = int(m.groupdict()['max_pfx'])
                continue

            # SOO Extcommunity: SOO:10.4.1.1:100
            m = p14.match(line)
            if m:
                sub_dict['soo'] = m.groupdict()['soo']
                continue

            # Weight: 9999
            m = p15.match(line)
            if m:
                sub_dict['weight'] = int(m.groupdict()['weight'])
                continue

            # Allow my ASN 10 times
            m = p16.match(line)
            if m:
                sub_dict['allow_as_in'] = int(m.groupdict()['asn'])
                continue

            # ASN override is enabled
            m = p17.match(line)
            if m:
                if m.groupdict()['status'] == 'enabled':
                    sub_dict['as_override'] = True
                else:
                    sub_dict['as_override'] = False
                continue

            # Peer ASN check is disabled
            m = p24.match(line)
            if m:
                sub_dict['peer_as_check_disabled'] = True
                continue

            # Inbound ip prefix-list configured is LIST123
            # Inbound route-map configured is PERMIT_ROUTE_IPV4_RM
            m = p18.match(line)
            if m:
                name = m.groupdict()['name']
                policy_type = m.groupdict()['type']

                if 'in_policy' not in sub_dict:
                    sub_dict['in_policy'] = {}

                if name not in sub_dict['in_policy']:
                    sub_dict['in_policy'][name] = {}

                sub_dict['in_policy'][name]['name'] = name
                sub_dict['in_policy'][name]['type'] = policy_type
                continue

            # Outbound ip prefix-list configured is LIST456
            # Outbound route-map configured is PERMIT_IPV6_RM
            m = p19.match(line)
            if m:
                name = m.groupdict()['name']
                policy_type = m.groupdict()['type']

                if 'out_policy' not in sub_dict:
                    sub_dict['out_policy'] = {}

                if name not in sub_dict['out_policy']:
                    sub_dict['out_policy'][name] = {}

                sub_dict['out_policy'][name]['name'] = name
                sub_dict['out_policy'][name]['type'] = policy_type
                continue

            # Default information originate, route-map PASS-ALL  Last End-of-RIB sent 0.000000 after session start
            # Default information originate  Last End-of-RIB sent 0.000000 after session start
            m = p20.match(line)
            if m:
                sub_dict['default_originate'] = True
                if m.groupdict()['map']:
                    sub_dict['default_originate_route_map'] = m.groupdict()['map']
                continue

            # First convergence 0.000000 after session start with 0 routes sent

            # Unsuppress-map ORIGINATE_IPV6 configured
            m = p21.match(line)
            if m:
                sub_dict['unsuppress_map'] = m.groupdict()['map']
                continue

            # Members of peer-template PEER1:
            # default: 10.186.201.1
            m = p22.match(line)
            if m:
                tem_peer = m.groupdict()['peer']
                continue

            m = p22_1.match(line)
            if m and tem_peer:
                if 'vrf' not in ret_dict['template'][tem_peer]:
                    ret_dict['template'][tem_peer]['vrf'] = {}

                vrf = m.groupdict()['vrf']

                if vrf not in ret_dict['template'][tem_peer]['vrf']:
                    ret_dict['template'][tem_peer]['vrf'][vrf] = {}

                if 'inheriting_peer' not in ret_dict['template'][tem_peer]['vrf'][vrf]:
                    ret_dict['template'][tem_peer]['vrf'][vrf]['inheriting_peer'] = {}

                nei = m.groupdict()['neighbor']

                if nei not in ret_dict['template'][tem_peer]['vrf'][vrf]['inheriting_peer']:
                    ret_dict['template'][tem_peer]['vrf'][vrf]['inheriting_peer'][nei] = {}

                ret_dict['template'][tem_peer]['vrf'][vrf]['inheriting_peer'][nei]\
                    ['inheriting_peer'] = nei
                    

                # reset tem_peer
                tem_peer = None
                continue

        return ret_dict


    def xml(self):
        out = self.device.execute(self.xml_command)

        etree_dict = {}
        sub_dict = {}
        # Remove junk characters returned by the device
        out = out.replace("]]>]]>", "")
        root = ET.fromstring(out)

        # top table root
        show_root = Common.retrieve_xml_child(root=root, key='show')
        # get xml namespace
        # {http://www.cisco.com/nxos:7.0.3.I7.1.:bgp}
        try:
            m = re.compile(r'(?P<name>\{[\S]+\})').match(show_root.tag)
            namespace = m.groupdict()['name']
        except Exception:
            return etree_dict

        # compare cli command
        Common.compose_compare_command(root=root, namespace=namespace,
                                expect_command=self.cli_command)

        # top table root
        root = Common.retrieve_xml_child(root=root, key='TABLE_neighbor')
        if not root:
            return etree_dict

        # -----   loop vrf  -----
        for peer_tree in root.findall('{}ROW_neighbor'.format(namespace)):
            # vrf
            try:
                template = peer_tree.find('{}templatepeer'.format(namespace)).text
            except Exception:
                break

            if 'template' not in etree_dict:
                etree_dict['template'] = {}
            if template not in etree_dict['template']:
                etree_dict['template'][template] = {}

            # <sourceif>loopback1</sourceif>
            try:
                etree_dict['template'][template]['source_interface'] = \
                    peer_tree.find('{}sourceif'.format(namespace)).text
            except Exception:
                pass

            # <lowmemexempt>true</lowmemexempt>
            try:
                if peer_tree.find('{}lowmemexempt'.format(namespace)).text == 'true':
                    etree_dict['template'][template]['low_mem_exempt'] = True
                else:
                    etree_dict['template'][template]['low_mem_exempt'] = False
            except Exception:
                pass

            # <ttlsecurity>false</ttlsecurity>
            if peer_tree.find('{}ttlsecurity'.format(namespace)).text == 'true':
                etree_dict['template'][template]['logging_neighbor_events'] = True
            else:
                etree_dict['template'][template]['logging_neighbor_events'] = False

            # <passiveonly>true</passiveonly>
            if peer_tree.find('{}passiveonly'.format(namespace)).text == 'true':
                etree_dict['template'][template]['passive_only'] = True
            else:
                etree_dict['template'][template]['passive_only'] = False

            # <localas-inactive>false</localas-inactive>
            if peer_tree.find('{}localas-inactive'.format(namespace)).text == 'true':
                etree_dict['template'][template]['local_as_inactive'] = True
            else:
                etree_dict['template'][template]['local_as_inactive'] = False

            # <remove-privateas>false</remove-privateas>
            if peer_tree.find('{}remove-privateas'.format(namespace)).text == 'true':
                etree_dict['template'][template]['remove_private_as'] = True
            else:
                etree_dict['template'][template]['remove_private_as'] = False

            # <ttllimit>100</ttllimit>
            try:
                etree_dict['template'][template]['external_bgp_peer_hops_limit'] = \
                    int(peer_tree.find('{}ttllimit'.format(namespace)).text)
            except Exception:
                pass

             # vrf table
            vrf_tree = peer_tree.find('{}TABLE_vrf'.format(namespace))
            if vrf_tree:
                # -----   loop vrf  -----
                for vrf_root in vrf_tree.findall('{}ROW_vrf'.format(namespace)):
                    # <vrf-name>default</vrf-name>
                    try:
                        vrf = vrf_root.find('{}vrf-name'.format(namespace)).text.lower()
                    except Exception:
                        continue

                    # inheritingpeer table
                    inherit_tree = vrf_root.find('{}TABLE_inheritingpeer'.format(namespace))
                    if not inherit_tree:
                        continue

                    # -----   loop inheritingpeer  -----
                    for inherit_root in inherit_tree.findall('{}ROW_inheritingpeer'
                                                             .format(namespace)):

                        # <inheritingpeer>10.186.201.1</inheritingpeer>
                        try:
                            inherit_peer = inherit_root.find('{}inheritingpeer'
                                                             .format(namespace)).text.lower()
                        except Exception:
                            continue
                        if 'vrf' not in etree_dict['template'][template]:
                            etree_dict['template'][template]['vrf'] = {}
                        if vrf not in etree_dict['template'][template]['vrf']:
                            etree_dict['template'][template]['vrf'][vrf] = {}

                        if 'inheriting_peer' not in etree_dict['template']\
                            [template]['vrf'][vrf]:
                            etree_dict['template'][template]['vrf'][vrf]\
                                ['inheriting_peer'] = {}
                            
                        if inherit_peer not in etree_dict['template']\
                            [template]['vrf'][vrf]['inheriting_peer']:
                            etree_dict['template'][template]['vrf'][vrf]\
                                ['inheriting_peer'][inherit_peer] = {}

                        etree_dict['template'][template]['vrf'][vrf]\
                                ['inheriting_peer'][inherit_peer]['inheriting_peer'] = inherit_peer


            # address_family table
            afi = peer_tree.find('{}TABLE_peraf'.format(namespace))

            # -----   loop address_family  -----
            for af_root in afi.findall('{}ROW_peraf'.format(namespace)):

                try:
                    # address_family
                    row_safi = af_root.find('{}TABLE_persaf'.format(namespace))
                    af_root = row_safi.find('{}ROW_persaf'.format(namespace))
                    af = af_root.find('{}per-af-name'.format(namespace)).text.lower()
                except Exception:
                    continue

                if 'address_family' not in etree_dict['template'][template]:
                    etree_dict['template'][template]['address_family'] = {}
                if af not in etree_dict['template'][template]['address_family']:
                    etree_dict['template'][template]['address_family'][af] = {}

                sub_dict = etree_dict['template'][template]['address_family'][af]

                # <conditionmap>DENY_ALL_RM</conditionmap>
                try:
                    sub_dict['condition_map'] = \
                        af_root.find('{}conditionmap'.format(namespace)).text
                except Exception:
                    pass

                # <advertisemap>BLOCK-ALL</advertisemap>
                try:
                    sub_dict['advertise_map'] = \
                        af_root.find('{}advertisemap'.format(namespace)).text
                except Exception:
                    pass

                # <advertisemapstatus>Advertise</advertisemapstatus>
                try:
                    sub_dict['advertise_map_status'] = \
                        af_root.find('{}advertisemapstatus'.format(namespace)).text.lower()
                except Exception:
                    pass

                try:
                    # <insoftreconfigallowed>false</insoftreconfigallowed>
                    if af_root.find('{}insoftreconfigallowed'.format(namespace)).text == 'true':
                        sub_dict['in_soft_reconfig_allowed'] = True
                    else:
                        sub_dict['in_soft_reconfig_allowed'] = False
                except Exception:
                    pass

                # <sendcommunity>true</sendcommunity>
                try:
                    if af_root.find('{}sendcommunity'.format(namespace)).text == 'true':
                        sub_dict['send_community'] = True
                    else:
                        sub_dict['send_community'] = False
                except Exception:
                    pass

                # <sendextcommunity>true</sendextcommunity>
                try:
                    if af_root.find('{}sendextcommunity'.format(namespace)).text == 'true':
                        sub_dict['send_ext_community'] = True
                    else:
                        sub_dict['send_ext_community'] = False
                except Exception:
                    pass

                # <thirdpartynexthop>false</thirdpartynexthop>
                try:
                    if af_root.find('{}thirdpartynexthop'.format(namespace)).text == 'true':
                        sub_dict['third_party_nexthop'] = True
                    else:
                        sub_dict['third_party_nexthop'] = False
                except Exception:
                    pass

                # <asoverride>true</asoverride>
                try:
                    if af_root.find('{}asoverride'.format(namespace)).text == 'true':
                        sub_dict['as_override'] = True
                    else:
                        sub_dict['as_override'] = False
                except Exception:
                    pass

                # <peerascheckdisabled>false</peerascheckdisabled>
                try:
                    if af_root.find('{}peerascheckdisabled'.format(namespace)).text == 'true':
                        sub_dict['peer_as_check_disabled'] = True
                    else:
                        sub_dict['peer_as_check_disabled'] = False
                except Exception:
                    pass

                # <rrconfigured>false</rrconfigured>
                try:
                    if af_root.find('{}rrconfigured'.format(namespace)).text == 'true':
                        sub_dict['rr_configured'] = True
                    else:
                        sub_dict['rr_configured'] = False
                except:
                    Exception

                # <localnexthop>0.0.0.0</localnexthop>
                try:
                    sub_dict['local_nexthop'] = \
                        af_root.find('{}localnexthop'.format(namespace)).text
                except Exception:
                    pass

                # <maxpfx>888888888</maxpfx>
                try:
                    sub_dict['max_pfx'] = \
                        int(af_root.find('{}maxpfx'.format(namespace)).text)
                except Exception:
                    pass

                # <soo>SOO:10.4.1.1:100</soo>
                try:
                    sub_dict['soo'] = \
                        af_root.find('{}soo'.format(namespace)).text
                except Exception:
                    pass

                # <weight>9999</weight>
                try:
                    sub_dict['weight'] = \
                        int(af_root.find('{}weight'.format(namespace)).text)
                except Exception:
                    pass

                # <allowasin>10</allowasin>
                try:
                    sub_dict['allow_as_in'] = \
                        int(af_root.find('{}allowasin'.format(namespace)).text)
                except Exception:
                    pass

                # <defaultoriginate>true</defaultoriginate>
                try:
                    if af_root.find('{}defaultoriginate'.format(namespace)).text == 'true':
                        sub_dict['default_originate'] = True
                    else:
                        sub_dict['default_originate'] = False
                except Exception:
                    pass

                # <defaultoriginatermap>PASS-ALL</defaultoriginatermap>
                try:
                    sub_dict['default_originate_route_map'] = \
                        af_root.find('{}defaultoriginatermap'.format(namespace)).text
                except Exception:
                    pass

                # <unsuppress-map>ORIGINATE_IPV6</unsuppress-map>
                try:
                    sub_dict['unsuppress_map'] = \
                        af_root.find('{}unsuppress-map'.format(namespace)).text
                except Exception:
                    pass
                

                # TABLE_inpolicy table
                policy = af_root.find('{}TABLE_inpolicy'.format(namespace))

                if policy:
                    # -----   loop in policy  -----
                    for policy_root in policy.findall('{}ROW_inpolicy'.format(namespace)):
                        try:
                            policy = policy_root.find('{}inpolicyname'.format(namespace)).text
                        except Exception:
                            continue

                        if 'in_policy' not in sub_dict:
                            sub_dict['in_policy'] = {}
                        if policy not in sub_dict['in_policy']:
                            sub_dict['in_policy'][policy] = {}

                        sub_dict['in_policy'][policy]['name'] = policy

                        # <inpolicytype>route-map</inpolicytype>
                        sub_dict['in_policy'][policy]['type'] = \
                            policy_root.find('{}inpolicytype'.format(namespace)).text

                # TABLE_outpolicy table
                policy = af_root.find('{}TABLE_outpolicy'.format(namespace))

                if policy:
                    # -----   loop in policy  -----
                    for policy_root in policy.findall('{}ROW_outpolicy'.format(namespace)):
                        try:
                            policy = policy_root.find('{}outpolicyname'.format(namespace)).text
                        except Exception:
                            continue
                        if 'out_policy' not in sub_dict:
                            sub_dict['out_policy'] = {}
                        if policy not in sub_dict['out_policy']:
                            sub_dict['out_policy'][policy] = {}

                        sub_dict['out_policy'][policy]['name'] = policy

                        # <outpolicytype>route-map</outpolicytype>
                        sub_dict['out_policy'][policy]['type'] = \
                            policy_root.find('{}outpolicytype'.format(namespace)).text

                                                                                                                         
        return etree_dict


# ==============================================================================
# Schema for:
# * 'show bgp vrf <vrf> <address_family>  policy statistics redistribute
# * 'show bgp vrf <vrf> <address_family>  policy statistics dampening'
# * 'show bgp vrf <vrf> <address_family>  policy statistics neighbor <neighbor>'
# ==============================================================================
class ShowBgpPolicyStatisticsSchema(MetaParser):
    """Schema for:
       show bgp [vrf <vrf>] <address_family>  policy statistics redistribute
       show bgp [vrf <vrf>] <address_family>  policy statistics dampening
       show bgp [vrf <vrf>] <address_family>  policy statistics neighbor <neighbor>
    """

    schema = {
        'vrf': {
            Any(): {
                Optional('rpm_handle_count'): int,
                Optional('route_map'): {
                    Any():{
                        Any(): {
                            'action': str,
                            'seq_num': int,
                            'total_accept_count': int,
                            'total_reject_count': int,
                            Optional('command'): {
                                'compare_count': int,
                                'match_count': int,
                                'command': str
                            }
                        },
                    },
                }
            },
        }
    }

# ==============================================================================
# Parser for:
# * 'show bgp vrf <vrf> <address_family>  policy statistics redistribute'
# * 'show bgp vrf <vrf> <address_family>  policy statistics dampening''
# * 'show bgp vrf <vrf> <address_family>  policy statistics neighbor <neighbor>'
# ==============================================================================
class ShowBgpPolicyStatisticsParser(ShowBgpPolicyStatisticsSchema):
    """Parser for:
        show bgp [vrf <vrf>] <address_family>  policy statistics redistribute
        show bgp [vrf <vrf>] <address_family>  policy statistics dampening
        show bgp [vrf <vrf>] <address_family>  policy statistics neighbor <neighbor>
        parser class implements detail parsing mechanisms for cli,xml output"""
    
    def cli(self, cmd,output=None):
        if output is None:
            out = self.device.execute(cmd)
        else:
            out = output
        
        # Init vars
        ret_dict = {}
        index = 1

        # extract vrf info if specified,
        # if not, vrf is default
        m = re.compile(r'^show +bgp +vrf +(?P<vrf>\S+)').match(cmd)
        if m:
            vrf = m.groupdict()['vrf']
            if vrf == 'all':
                vrf = ''
        else:
            vrf = 'default'
        p1 = re.compile(r'^Details +for +VRF +'
                            r'(?P<vrf>[\w\-]+)$')
        p2 = re.compile(r'^Total +count +for +(?P<type>\w+) +rpm +handles: +'
                            r'(?P<handles>\d+)$')
        p3 = re.compile(r'^BGP +policy +statistics +not +available$')
        p4 = re.compile(r'^route\-map +(?P<name>\S+) +'
                            r'(?P<action>\w+) +(?P<seqnum>\d+)$')
        p5 = re.compile(r'^(?P<command>[\w\s\-\>]+) +'
                            r'C: +(?P<compare_count>\d+) +'
                            r'M: +(?P<match_count>\d+)$')
        p6 = re.compile(r'^Total +accept +count +for +policy: +'
                            r'(?P<total_accept_count>\d+)$')
        p7 = re.compile(r'^Total +reject +count +for +policy: +'
                            r'(?P<total_reject_count>\d+)$')

        for line in out.splitlines():
            line = line.strip()

            # Details for VRF default
            m = p1.match(line)
            if m:
                vrf = m.groupdict()['vrf']
                nei_flag = True
                continue

            # No such neighbor
            if re.compile(r'No +such +neighbor$').match(line):
                nei_flag = False

            # Total count for redistribute rpm handles: 1
            # Total count for neighbor rpm handles: 1
            # Total count for dampening rpm handles: 1
            m = p2.match(line)

            # BGP policy statistics not available
            m1 = p3.match(line)

            if m or m1:
                if 'vrf' not in ret_dict:
                    ret_dict['vrf'] = {}

                if vrf not in ret_dict['vrf']:
                    ret_dict['vrf'][vrf] = {}

                ret_dict['vrf'][vrf]['rpm_handle_count'] = \
                    int(m.groupdict()['handles']) if m else 0
                continue

            # C: No. of comparisions, M: No. of matches

            # route-map Filter-pip deny 10
            # route-map ADD_RT_400_400 permit 10
            # route-map RMAP_DIRECT->BGP_IPV4 permit 10
            m = p4.match(line)
            if m:
                name = m.groupdict()['name']

                if 'vrf' not in ret_dict:
                    ret_dict['vrf'] = {}

                if vrf not in ret_dict['vrf']:
                    ret_dict['vrf'][vrf] = {}

                if 'route_map' not in ret_dict['vrf'][vrf]:
                    ret_dict['vrf'][vrf]['route_map'] = {}

                if name not in ret_dict['vrf'][vrf]['route_map']:
                    ret_dict['vrf'][vrf]['route_map'][name] = {}
                    index = 1
                else:
                    index += 1

                if index not in ret_dict['vrf'][vrf]['route_map'][name]:
                    ret_dict['vrf'][vrf]['route_map'][name][index] = {}

                ret_dict['vrf'][vrf]['route_map'][name][index]['action'] = \
                    m.groupdict()['action']

                ret_dict['vrf'][vrf]['route_map'][name][index]['seq_num'] = \
                    int(m.groupdict()['seqnum'])
                continue

            #   match ip address prefix-list pip-prefix                    C: 0      M: 0 
            #   match ip address prefix-list DIRECT->BGP_IPV4              C: 16     M: 0 
            m = p5.match(line)
            if m:
                command = m.groupdict()['command'].strip()

                if 'command' not in ret_dict['vrf'][vrf]['route_map'][name][index]:
                    ret_dict['vrf'][vrf]['route_map'][name][index]['command'] = {}

                ret_dict['vrf'][vrf]['route_map'][name][index]['command']\
                    ['compare_count'] = int(m.groupdict()['compare_count'])

                ret_dict['vrf'][vrf]['route_map'][name][index]['command']\
                    ['match_count'] = int(m.groupdict()['match_count'])

                ret_dict['vrf'][vrf]['route_map'][name][index]['command']\
                    ['command'] = command
                continue

            # Total accept count for policy: 0
            m = p6.match(line)
            if m:
                ret_dict['vrf'][vrf]['route_map'][name][index]['total_accept_count'] = \
                    int(m.groupdict()['total_accept_count'])
                continue

            # Total reject count for policy: 0
            m = p7.match(line)
            if m:
                ret_dict['vrf'][vrf]['route_map'][name][index]['total_reject_count'] = \
                    int(m.groupdict()['total_reject_count'])
                continue

        return ret_dict


    def xml(self, cmd):
        out = self.device.execute('{cmd} | xml'.format(cmd=cmd))

        etree_dict = {}
        neighbor = None
        # Remove junk characters returned by the device
        out = out.replace("]]>]]>", "")
        root = ET.fromstring(out)

        # top table root
        show_root = Common.retrieve_xml_child(root=root, key='show')
        # get xml namespace
        # {http://www.cisco.com/nxos:7.0.3.I7.1.:bgp}
        try:
            m = re.compile(r'(?P<name>\{[\S]+\})').match(show_root.tag)
            namespace = m.groupdict()['name']
        except Exception:
            return etree_dict

        # compare cli command
        Common.compose_compare_command(root=root, namespace=namespace,
                                       expect_command=cmd)

        # get neighbor
        nei = Common.retrieve_xml_child(root=root, key='__XML__PARAM__neighbor-id')

        if hasattr(nei, 'tag'):
            for item in list(nei):
                if '__XML__value' in item.tag:
                    neighbor = item.text
                    continue

                # cover the senario that __readonly__ may be mssing when
                # there are values in the output
                if '__readonly__' in item.tag:
                    root = list(item)[0]
                else:
                    root = item
        else:
            # top table rootl
            root = Common.retrieve_xml_child(root=root, key='TABLE_vrf')

        if not root:
            return etree_dict

        # -----   loop vrf  -----
        for vrf_tree in root.findall('{}ROW_vrf'.format(namespace)):
            # vrf
            try:
                vrf = vrf_tree.find('{}vrf-name-polstats'.format(namespace)).text
            except Exception:
                break

            if 'vrf' not in etree_dict:
                etree_dict['vrf'] = {}
            if vrf not in etree_dict['vrf']:
                etree_dict['vrf'][vrf] = {}

            # <rpm-handle-count>1</rpm-handle-count>
            etree_dict['vrf'][vrf]['rpm_handle_count'] = \
                int(vrf_tree.find('{}rpm-handle-count'.format(namespace)).text)

             # route_map table
            rpm_tree = vrf_tree.find('{}TABLE_rmap'.format(namespace))
            if not rpm_tree:
                continue

            # -----   loop route_map  -----
            for rmp_root in rpm_tree.findall('{}ROW_rmap'.format(namespace)):
                # route map
                try:
                    name = rmp_root.find('{}name'.format(namespace)).text
                    name = name.replace('&gt;', '>')
                except Exception:
                    continue

                if 'route_map' not in etree_dict['vrf'][vrf]:
                    etree_dict['vrf'][vrf]['route_map'] = {}

                if name not in etree_dict['vrf'][vrf]['route_map']:
                    etree_dict['vrf'][vrf]['route_map'][name] = {}
                    # initial index
                    index = 1
                else:
                    index += 1
                    
                if index not in etree_dict['vrf'][vrf]['route_map'][name]:
                    etree_dict['vrf'][vrf]['route_map'][name][index] = {}


                # <action>deny</action>
                try:
                    etree_dict['vrf'][vrf]['route_map'][name][index]['action'] = \
                        rmp_root.find('{}action'.format(namespace)).text
                except Exception:
                    pass

                # <seqnum>10</seqnum>
                try:
                    etree_dict['vrf'][vrf]['route_map'][name][index]['seq_num'] = \
                        int(rmp_root.find('{}seqnum'.format(namespace)).text)
                except Exception:
                    pass

                # <totalacceptcount>0</totalacceptcount>
                try:
                    etree_dict['vrf'][vrf]['route_map'][name][index]['total_accept_count'] = \
                        int(rmp_root.find('{}totalacceptcount'.format(namespace)).text)
                except Exception:
                    pass

                # <totalrejectcount>2</totalrejectcount>
                try:
                    etree_dict['vrf'][vrf]['route_map'][name][index]['total_reject_count'] = \
                        int(rmp_root.find('{}totalrejectcount'.format(namespace)).text)
                except Exception:
                    pass


                # TABLE_cmd table
                command = rmp_root.find('{}TABLE_cmd'.format(namespace))

                if not command:
                    continue

                # -----   loop command  -----
                for command_root in command.findall('{}ROW_cmd'.format(namespace)):
                    try:
                        cmd_str = command_root.find('{}command'.format(namespace)).text.strip()
                        cmd_str = cmd_str.replace('&gt;', '>')
                    except Exception:
                        continue

                    if 'command' not in etree_dict['vrf'][vrf]['route_map'][name][index]:
                        etree_dict['vrf'][vrf]['route_map'][name][index]['command'] = {}

                    # command
                    etree_dict['vrf'][vrf]['route_map'][name][index]\
                        ['command']['command'] = cmd_str

                    # <comparecount>2</comparecount>
                    try:
                        etree_dict['vrf'][vrf]['route_map'][name][index]\
                            ['command']['compare_count'] = \
                                int(command_root.find('{}comparecount'.format(namespace)).text)
                    except Exception:
                        pass
                    
                    # <matchcount>0</matchcount>
                    try:
                        etree_dict['vrf'][vrf]['route_map'][name][index]\
                            ['command']['match_count'] = \
                                int(command_root.find('{}matchcount'.format(namespace)).text)
                    except Exception:
                        pass
        return etree_dict

# ===============================================================================
# Parser for 'show bgp vrf <vrf> <address_family> policy statistics redistribute'
# ===============================================================================
class ShowBgpPolicyStatisticsRedistribute(ShowBgpPolicyStatisticsParser):
    """Parser for:
        show bgp [vrf <vrf>] <address_family> policy statistics redistribute
        parser class implements detail parsing mechanisms for cli,xml output"""

    cli_command = ['show bgp vrf {vrf} {address_family} policy statistics redistribute',\
                   'show bgp {address_family} policy statistics redistribute']

    xml_command = ['show bgp vrf {vrf} {address_family} policy statistics redistribute', \
                   'show bgp {address_family} policy statistics redistribute']
    exclude = [
      'compare_count',
      'total_reject_count',
      'match_count',
      'total_accept_count']
    def cli(self, address_family, vrf='',output=None):
        if output is None:
            if vrf:
                cmd = self.cli_command[0].format(vrf=vrf, address_family=address_family)
            else:
                cmd = self.cli_command[1].format(address_family=address_family)
        else:
            cmd = ""

        return super().cli(cmd=cmd, output=output)

    def xml(self, address_family, vrf=''):

        if vrf:
            cmd = self.xml_command[0].format(vrf=vrf, address_family=address_family)
        else:
            cmd = self.xml_command[1].format(address_family=address_family)


        return super().xml(cmd=cmd)

# ==================================================================================
# Parser for 'show bgp vrf <vrf> <address_family> policy statistics neighbor <WORD>'
# ==================================================================================
class ShowBgpPolicyStatisticsNeighbor(ShowBgpPolicyStatisticsParser):
    """Parser for:
        show bgp [vrf <vrf>] <address_family> policy statistics neighbor <neighbor>
        parser class implements detail parsing mechanisms for cli,xml output"""

    cli_command = ['show bgp vrf {vrf} {address_family} policy statistics neighbor {neighbor}', \
                   'show bgp {address_family} policy statistics neighbor {neighbor}']

    xml_command = ['show bgp vrf {vrf} {address_family} policy statistics neighbor {neighbor}', \
                   'show bgp {address_family} policy statistics neighbor {neighbor}']

    def cli(self, address_family, neighbor, vrf='', output=None):
        if output is None:
            if vrf:
                cmd = self.cli_command[0].format(vrf=vrf, address_family=address_family, neighbor=neighbor)
            else:
                cmd = self.cli_command[1].format(address_family=address_family, neighbor=neighbor)

        return super().cli(cmd=cmd,output=output)

    def xml(self, address_family, neighbor, vrf=''):
        if vrf:
            cmd = self.xml_command[0].format(vrf=vrf, address_family=address_family, neighbor=neighbor)
        else:
            cmd = self.xml_command[1].format(address_family=address_family, neighbor=neighbor)

        return super().xml(cmd=cmd)

# ============================================================================
# Parser for 'show bgp vrf <vrf> <address_family> policy statistics dampening'
# ============================================================================
class ShowBgpPolicyStatisticsDampening(ShowBgpPolicyStatisticsParser):
    """Parser for:
        show bgp [vrf <vrf>] <address_family> policy statistics dampening
        parser class implements detail parsing mechanisms for cli,xml output"""
    cli_command = ['show bgp vrf {vrf} {address_family} policy statistics dampening','show bgp {address_family} policy statistics dampening']
    xml_command = ['show bgp vrf {vrf} {address_family} policy statistics dampening','show bgp {address_family} policy statistics dampening']

    def cli(self, address_family, vrf='',output=None):
        if output is None:
            if vrf:
                cmd = self.cli_command[0].format(vrf=vrf, address_family=address_family)
            else:
                cmd = self.cli_command[1].format(address_family=address_family)
        else:
            cmd = ""
        return super().cli(cmd=cmd,output=output)

    def xml(self, address_family, vrf=''):

        if vrf:
            cmd = self.xml_command[0].format(vrf=vrf, address_family=address_family)
        else:
            cmd = self.xml_command[1].format(vrf=vrf, address_family=address_family)

        return super().xml(cmd=cmd)


# =========================================
# Schema for 'show bgp sessions vrf <WORD>'
# =========================================
class ShowBgpSessionsSchema(MetaParser):
    """Schema for:
       show bgp sessions
       show bgp sessions vrf <WROD>
    """

    schema = {
        'total_peers': int,
        'total_established_peers': int,
        'local_as': int,
        'vrf': {
            Any(): {
                'local_as': int,
                'vrf_peers': int,
                'vrf_established_peers': int,
                'router_id': str,
                Optional('neighbor'): {
                    Any(): {
                        'connections_dropped': int,
                        'remote_as': int,
                        'last_flap': str,
                        'last_read': str,
                        'last_write': str,
                        'state': str,
                        'local_port': int,
                        'remote_port': int,
                        'notifications_sent': int,
                        'notifications_received': int,
                        Optional('linklocal_interfaceport'): str,
                    },
                }
            },
        }
    }

# =========================================
# Parser for 'show bgp sessions vrf <WORD>'
# =========================================
class ShowBgpSessions(ShowBgpSessionsSchema):
    """Parser for:
        show bgp sessions"""

    cli_command = ['show bgp sessions vrf {vrf}','show bgp sessions']
    xml_command = ['show bgp sessions vrf {vrf} | xml','show bgp sessions | xml']
    exclude = ['last_read', 'last_write']

    def cli(self, vrf='',output=None):
        if output is None:
            if vrf:
                cmd = self.cli_command[0].format(vrf=vrf)
            else:
                 cmd = self.cli_command[1]
            out = self.device.execute(cmd)
        else:
            out = output
        
        # Init vars
        ret_dict = {}
        status_map = {'I': 'idle',
                      'A': 'active',
                      'O': 'open',
                      'E': 'established',
                      'C': 'closing',
                      'S': 'shutdown'}
        # Total peers 4, established peers 3
        p1 = re.compile(r'^Total +peers +(?P<total>\d+), +'
                            r'established +peers +(?P<established>\d+)$')
        # ASN 100
        p2 = re.compile(r'^ASN +(?P<asn>\d+)$')
        # VRF default, local ASN 100
        p3 = re.compile(r'^VRF +(?P<vrf>\S+), +'
                            r'local +ASN +(?P<asn>\d+)$')
        # peers 4, established peers 3, local router-id 10.1.1.1
        p4 = re.compile(r'^peers +(?P<peer>\d+), +'
                            r'established +peers +(?P<established>\d+), +'
                            r'local +router\-id +(?P<id>[\w\.\:]+)$')
        # 10.51.1.101        300 2     00:30:01|never   |never    I   0/0          2/0
        p5 = re.compile(r'^(?P<nei>[\w\.\:]+) +'
                            r'(?P<asn>\d+) +'
                            r'(?P<dropped>\d+) +'
                            r'(?P<last_flap>[\w\.\:]+) *\|'
                            r'(?P<last_read>[\w\.\:]+) *\|'
                            r'(?P<last_write>[\w\.\:]+) +'
                            r'(?P<state>[a-zA-Z]) +'
                            r'(?P<local_port>\d+)\/'
                            r'(?P<remote_port>\d+) +'
                            r'(?P<notifications_sent>\d+)\/'
                            r'(?P<notifications_received>\d+)$')
        # fe80::7e21:eff:fe2e:cc58%Ethernet1/2
        # fe80::205:ff:fe00:15%port-channel15
        p6_1 = re.compile(r'^(?P<nei>[a-zA-Z0-9\.\:\/\[\]\,]+)%'
                           r'(?P<linklocal_interfaceport>[a-zA-Z0-9\.\-\:\/\[\]\,]+)$')
        #                     1 0     00:00:18|00:00:17|00:00:17 E   20230/179        0/0
        p6_2 = re.compile(r'^(?P<asn>\d+) +'
                            r'(?P<dropped>\d+) +'
                            r'(?P<last_flap>[\w\.\:]+) *\|'
                            r'(?P<last_read>[\w\.\:]+) *\|'
                            r'(?P<last_write>[\w\.\:]+) +'
                            r'(?P<state>[a-zA-Z]) +'
                            r'(?P<local_port>\d+)\/'
                            r'(?P<remote_port>\d+) +'
                            r'(?P<notifications_sent>\d+)\/'
                            r'(?P<notifications_received>\d+)$')
        # 4.4.4.1         4258745628
        p7_1 = re.compile(r'^(?P<nei>[\da-f.\:]+) +'
                            r'(?P<asn>\d+)$')
        #                     0     00:01:39|00:00:11|00:00:20 E   179/21890      0/0
        p7_2 = re.compile(r'^(?P<dropped>\d+) +'
                            r'(?P<last_flap>[\w\.\:]+) *\|'
                            r'(?P<last_read>[\w\.\:]+) *\|'
                            r'(?P<last_write>[\w\.\:]+) +'
                            r'(?P<state>[a-zA-Z]) +'
                            r'(?P<local_port>\d+)\/'
                            r'(?P<remote_port>\d+) +'
                            r'(?P<notifications_sent>\d+)\/'
                            r'(?P<notifications_received>\d+)$')

        for line in out.splitlines():
            line = line.strip()

            # Total peers 4, established peers 3
            m = p1.match(line)
            if m:
                ret_dict['total_peers'] = int(m.groupdict()['total'])
                ret_dict['total_established_peers'] = \
                    int(m.groupdict()['established'])
                continue

            # ASN 100
            m = p2.match(line)
            if m:
                ret_dict['local_as'] = int(m.groupdict()['asn'])
                continue


            # VRF default, local ASN 100
            m = p3.match(line)
            if m:
                vrf = m.groupdict()['vrf']
                if 'vrf' not in ret_dict:
                    ret_dict['vrf'] = {}
                if vrf not in ret_dict['vrf']:
                    ret_dict['vrf'][vrf] = {}
                ret_dict['vrf'][vrf]['local_as'] = \
                    int(m.groupdict()['asn'])
                continue

            # peers 4, established peers 3, local router-id 10.1.1.1
            m = p4.match(line)
            if m:
                ret_dict['vrf'][vrf]['vrf_peers'] = \
                    int(m.groupdict()['peer'])

                ret_dict['vrf'][vrf]['vrf_established_peers'] = \
                    int(m.groupdict()['established'])
                    
                ret_dict['vrf'][vrf]['router_id'] = \
                    m.groupdict()['id']
                continue

            # 10.51.1.101        300 2     00:30:01|never   |never    I   0/0          2/0
            m = p5.match(line)
            if m:
                group = m.groupdict()

                nei = group['nei']
                if 'neighbor' not in ret_dict['vrf'][vrf]:
                    ret_dict['vrf'][vrf]['neighbor'] = {}
                if nei not in ret_dict['vrf'][vrf]['neighbor']:
                    ret_dict['vrf'][vrf]['neighbor'][nei] = {}

                ret_dict['vrf'][vrf]['neighbor'][nei]['remote_as'] = \
                    int(group['asn'])

                ret_dict['vrf'][vrf]['neighbor'][nei]['connections_dropped'] = \
                    int(group['dropped'])

                ret_dict['vrf'][vrf]['neighbor'][nei]['last_flap'] = \
                    group['last_flap']

                ret_dict['vrf'][vrf]['neighbor'][nei]['last_read'] = \
                    group['last_read']

                ret_dict['vrf'][vrf]['neighbor'][nei]['last_write'] = \
                    group['last_write']

                ret_dict['vrf'][vrf]['neighbor'][nei]['state'] = \
                    status_map[group['state']]

                ret_dict['vrf'][vrf]['neighbor'][nei]['local_port'] = \
                    int(group['local_port'])

                ret_dict['vrf'][vrf]['neighbor'][nei]['remote_port'] = \
                    int(group['remote_port'])

                ret_dict['vrf'][vrf]['neighbor'][nei]['notifications_sent'] = \
                    int(group['notifications_sent'])

                ret_dict['vrf'][vrf]['neighbor'][nei]['notifications_received'] = \
                    int(group['notifications_received'])
                continue

            # fe80::7e21:eff:fe2e:cc58%Ethernet1/2
            #linklocal_interfaceport
            m = p6_1.match(line)
            if m:
                group = m.groupdict()
                nei = group['nei']
                if 'neighbor' not in ret_dict['vrf'][vrf]:
                    ret_dict['vrf'][vrf]['neighbor'] = {}
                if nei not in ret_dict['vrf'][vrf]['neighbor']:
                    ret_dict['vrf'][vrf]['neighbor'][nei] = {}
                ret_dict['vrf'][vrf]['neighbor'][nei]['linklocal_interfaceport'] = \
                    group['linklocal_interfaceport']
                continue

            #                     1 0     00:00:18|00:00:17|00:00:17 E   20230/179        0/0
            m = p6_2.match(line)
            if m:
                group = m.groupdict()

                ret_dict['vrf'][vrf]['neighbor'][nei]['remote_as'] = \
                    int(group['asn'])

                ret_dict['vrf'][vrf]['neighbor'][nei]['connections_dropped'] = \
                    int(group['dropped'])

                ret_dict['vrf'][vrf]['neighbor'][nei]['last_flap'] = \
                    group['last_flap']

                ret_dict['vrf'][vrf]['neighbor'][nei]['last_read'] = \
                    group['last_read']

                ret_dict['vrf'][vrf]['neighbor'][nei]['last_write'] = \
                    group['last_write']

                ret_dict['vrf'][vrf]['neighbor'][nei]['state'] = \
                    status_map[group['state']]

                ret_dict['vrf'][vrf]['neighbor'][nei]['local_port'] = \
                    int(group['local_port'])

                ret_dict['vrf'][vrf]['neighbor'][nei]['remote_port'] = \
                    int(group['remote_port'])

                ret_dict['vrf'][vrf]['neighbor'][nei]['notifications_sent'] = \
                    int(group['notifications_sent'])

                ret_dict['vrf'][vrf]['neighbor'][nei]['notifications_received'] = \
                    int(group['notifications_received'])
                continue

            # 4.4.4.1         4258745628
            m = p7_1.match(line)
            if m:
                group = m.groupdict()

                nei = group['nei']
                if 'neighbor' not in ret_dict['vrf'][vrf]:
                    ret_dict['vrf'][vrf]['neighbor'] = {}
                if nei not in ret_dict['vrf'][vrf]['neighbor']:
                    ret_dict['vrf'][vrf]['neighbor'][nei] = {}

                ret_dict['vrf'][vrf]['neighbor'][nei]['remote_as'] = \
                    int(group['asn'])
                continue

            m = p7_2.match(line)
            if m:
                group = m.groupdict()

                ret_dict['vrf'][vrf]['neighbor'][nei]['connections_dropped'] = \
                    int(group['dropped'])

                ret_dict['vrf'][vrf]['neighbor'][nei]['last_flap'] = \
                    group['last_flap']

                ret_dict['vrf'][vrf]['neighbor'][nei]['last_read'] = \
                    group['last_read']

                ret_dict['vrf'][vrf]['neighbor'][nei]['last_write'] = \
                    group['last_write']

                ret_dict['vrf'][vrf]['neighbor'][nei]['state'] = \
                    status_map[group['state']]

                ret_dict['vrf'][vrf]['neighbor'][nei]['local_port'] = \
                    int(group['local_port'])

                ret_dict['vrf'][vrf]['neighbor'][nei]['remote_port'] = \
                    int(group['remote_port'])

                ret_dict['vrf'][vrf]['neighbor'][nei]['notifications_sent'] = \
                    int(group['notifications_sent'])

                ret_dict['vrf'][vrf]['neighbor'][nei]['notifications_received'] = \
                    int(group['notifications_received'])
                continue

        return ret_dict

    def xml(self, vrf=''):
        if vrf:
            cmd = self.xml_command[0].format(vrf=vrf)
            cli_cmd = self.cli_command[0].format(vrf=vrf)
        else:
            cmd = self.xml_command[1]
            cli_cmd = self.cli_command[1]

        out = self.device.execute(cmd)

        etree_dict = {}

        # Remove junk characters returned by the device
        out = out.replace("]]>]]>", "")
        root = ET.fromstring(out)

        # top table root
        show_root = Common.retrieve_xml_child(root=root, key='show')
        # get xml namespace
        # {http://www.cisco.com/nxos:7.0.3.I7.1.:bgp}
        try:
            m = re.compile(r'(?P<name>\{[\S]+\})').match(show_root.tag)
            namespace = m.groupdict()['name']
        except Exception:
            return etree_dict

        # compare cli command
        Common.compose_compare_command(root=root, namespace=namespace,
                                       expect_command=cli_cmd)

        ret = Common.retrieve_xml_child(
                root=root,
                key='__readonly__')

        if hasattr(ret, 'tag'):
            # get total_peers                
            try:
                total_peers = ret.find('{}totalpeers'.format(namespace)).text
                etree_dict['total_peers'] = int(total_peers)
            except Exception:
                pass

            # get total_established_peers            
            try:
                total_established_peers = ret.find(
                    '{}totalestablishedpeers'.format(namespace)).text
                etree_dict['total_established_peers'] = int(total_established_peers)
            except Exception:
                pass

            # get local_as               
            try:
                local_as = ret.find('{}localas'.format(namespace)).text
                etree_dict['local_as'] = int(local_as)
            except Exception:
                pass

        else:
            # output is empty
            return etree_dict

        # find Vrf root
        root = ret.find('{}TABLE_vrf'.format(namespace))

        if not root:
            return etree_dict

        # -----   loop vrf  -----
        for vrf_tree in root.findall('{}ROW_vrf'.format(namespace)):
            # vrf
            try:
                vrf = vrf_tree.find('{}vrf-name-out'.format(namespace)).text
            except Exception:
                break

            if 'vrf' not in etree_dict:
                etree_dict['vrf'] = {}
            if vrf not in etree_dict['vrf']:
                etree_dict['vrf'][vrf] = {}

            # <local-as>333</local-as>
            etree_dict['vrf'][vrf]['local_as'] = \
                int(vrf_tree.find('{}local-as'.format(namespace)).text)

            # <vrfpeers>3</vrfpeers>
            etree_dict['vrf'][vrf]['vrf_peers'] = \
                int(vrf_tree.find('{}vrfpeers'.format(namespace)).text)

            # <vrfestablishedpeers>2</vrfestablishedpeers>
            etree_dict['vrf'][vrf]['vrf_established_peers'] = \
                int(vrf_tree.find('{}vrfestablishedpeers'.format(namespace)).text)
                
            # <router-id>10.106.0.6</router-id>
            etree_dict['vrf'][vrf]['router_id'] = \
                vrf_tree.find('{}router-id'.format(namespace)).text
                
             # Neighbor table
            nei_tree = vrf_tree.find('{}TABLE_neighbor'.format(namespace))
            if not nei_tree:
                continue

            # -----   loop neighbors  -----
            for nei_root in nei_tree.findall('{}ROW_neighbor'.format(namespace)):
                # neighbor
                try:
                    nei = nei_root.find('{}neighbor-id'.format(namespace)).text
                except Exception:
                    continue

                if 'neighbor' not in etree_dict['vrf'][vrf]:
                    etree_dict['vrf'][vrf]['neighbor'] = {}

                if nei not in etree_dict['vrf'][vrf]['neighbor']:
                    etree_dict['vrf'][vrf]['neighbor'][nei] = {}

                # <connectionsdropped>0</connectionsdropped>
                try:
                    etree_dict['vrf'][vrf]['neighbor'][nei]['connections_dropped'] = \
                        int(nei_root.find('{}connectionsdropped'.format(namespace)).text)
                except Exception:
                    pass

                # <remoteas>333</remoteas>
                try:
                    etree_dict['vrf'][vrf]['neighbor'][nei]['remote_as'] = \
                        int(nei_root.find('{}remoteas'.format(namespace)).text)
                except Exception:
                    pass

                # <lastflap>PT1H4M41S</lastflap>
                try:
                    ret = nei_root.find('{}lastflap'.format(namespace)).text
                    ret = Common.convert_xml_time(ret)
                    etree_dict['vrf'][vrf]['neighbor'][nei]['last_flap'] = \
                        'never' if 'P' in ret else ret
                except Exception:
                    etree_dict['vrf'][vrf]['neighbor'][nei]['last_flap'] = 'never'
                    
                # <lastread>PT47S</lastread>
                try:
                    ret = nei_root.find('{}lastread'.format(namespace)).text
                    ret = Common.convert_xml_time(ret)
                    etree_dict['vrf'][vrf]['neighbor'][nei]['last_read'] = \
                        'never' if 'P' in ret else ret
                except Exception:
                    etree_dict['vrf'][vrf]['neighbor'][nei]['last_read'] = 'never'
                    
                # <lastwrite>PT15S</lastwrite>
                try:
                    ret = nei_root.find('{}lastwrite'.format(namespace)).text
                    ret = Common.convert_xml_time(ret)
                    etree_dict['vrf'][vrf]['neighbor'][nei]['last_write'] = \
                        'never' if 'P' in ret else ret
                except Exception:
                    etree_dict['vrf'][vrf]['neighbor'][nei]['last_write'] = 'never'
                    
                # <state>Established</state>
                try:
                    etree_dict['vrf'][vrf]['neighbor'][nei]['state'] = \
                        nei_root.find('{}state'.format(namespace)).text.lower()
                except Exception:
                    pass
                    
                # <localport>179</localport>
                try:
                    etree_dict['vrf'][vrf]['neighbor'][nei]['local_port'] = \
                        int(nei_root.find('{}localport'.format(namespace)).text)
                except Exception:
                    pass
                    
                # <remoteport>48392</remoteport>
                try:
                    etree_dict['vrf'][vrf]['neighbor'][nei]['remote_port'] = \
                        int(nei_root.find('{}remoteport'.format(namespace)).text)
                except Exception:
                    pass
                    
                # <notificationssent>0</notificationssent>
                try:
                    etree_dict['vrf'][vrf]['neighbor'][nei]['notifications_sent'] = \
                        int(nei_root.find('{}notificationssent'.format(namespace)).text)
                except Exception:
                    pass
                    
                # <notificationsreceived>0</notificationsreceived>
                try:
                    etree_dict['vrf'][vrf]['neighbor'][nei]['notifications_received'] = \
                        int(nei_root.find('{}notificationsreceived'.format(namespace)).text)
                except Exception:
                    pass                    

        return etree_dict


# ========================================================
# Schema for 'show bgp <address_family> labels vrf <WORD>'
# ========================================================
class ShowBgpLabelsSchema(MetaParser):
    """Schema for:
       show bgp <address_family> labels
       show bgp <address_family> labels vrf <WROD>
    """

    schema = {
        'vrf': {
            Any(): {
                'address_family': {
                    Any(): {
                        'table_version': int,
                        'router_id': str,
                        Optional('prefix'): {
                            Any(): {
                                'index': {
                                    Any(): {
                                        'status': str,
                                        'best_path': bool,
                                        Optional('type'): str,
                                        Optional('status_code'): str,
                                        Optional('best_code'): str,
                                        Optional('type_code'): str,
                                        'nexthop': str,
                                        'in_label': str,
                                        'out_label': str,
                                        Optional('vpn'): str,
                                        Optional('hold_down'): str,
                                    },
                                }
                            },
                        },
                        Optional('route_distinguisher'): {
                            Any(): {
                                Optional('rd_vrf'): str,
                                'prefix': {
                                    Any(): {
                                        'index': {
                                            Any(): {
                                                'status': str,
                                                'best_path': bool,
                                                Optional('type'): str,
                                                Optional('status_code'): str,
                                                Optional('best_code'): str,
                                                Optional('type_code'): str,
                                                'nexthop': str,
                                                'in_label': str,
                                                'out_label': str,
                                                Optional('vpn'): str,
                                                Optional('hold_down'): str,
                                            },
                                        }
                                    },
                                }
                            },
                        }
                    },
                }
            },
        }
    }

# ========================================================
# Parser for 'show bgp <address_family> labels vrf <WORD>'
# ========================================================
class ShowBgpLabels(ShowBgpLabelsSchema):
    """Parser for:
        show bgp <address_family> labels [vrf <WROD>]"""

    cli_command = ['show bgp {address_family} labels vrf {vrf}','show bgp {address_family} labels']
    xml_command = ['show bgp {address_family} labels vrf {vrf} | xml','show bgp {address_family} labels | xml']
    exclude = [
      'table_version']

    def cli(self, address_family, vrf='',output=None):
        assert address_family in ['ipv4 unicast', 'ipv4 multicast',
                                  'ipv6 unicast', 'ipv6 multicast',
                                  'vpnv4 unicast', 'vpnv6 unicast']


        if output is None:
            if vrf:
                cmd = self.cli_command[0].format(address_family=address_family, vrf=vrf)
            else:
                cmd = self.cli_command[1].format(address_family=address_family)
            out = self.device.execute(cmd)
        else:
            out = output

        # Init vars
        ret_dict = {}
        status_map = {'*': 'valid',
                      's': 'suppressed,',
                      'x': 'deleted',
                      'S': 'stale',
                      'd': 'dampened',
                      'h': 'history',
                      '>': 'best'}
        path_type_map = {'i': 'internal',
                         'e': 'external',
                         'c': 'confed',
                         'l': 'local',
                         'r': 'redist',
                         'a': 'aggregate',
                         'I': 'injected'}
        p1 = re.compile(r'^BGP +routing +table +information +for +VRF +(?P<vrf>\S+), +'
                            r'address +family +(?P<af>[\w\s]+)$')
        p2 = re.compile(r'^BGP +table +version +is +(?P<ver>\d+), +'
                            r'(L|l)ocal +(R|r)outer +ID +is +(?P<router_id>[\w\.\:]+)$')
        p4 = re.compile(r'^Route +Distinguisher: +(?P<rd>[\w\.\:]+) +'
                            r'\(VRF +(?P<vrf>\S+)\)$')
        p3 = re.compile(r'^(?P<status>s|S|x|d|h|\*)?'
                            r'(?P<best>\>)?'
                            r' *(?P<type_code>i|e|c|l|a|r|I)'
                            r'(?P<prefix>[\w\/\.\:]+)?'
                            r' +(?P<next_hop>[\w\/\.\:]+)'
                            r'(?: +(?P<in_label>\w+)\/(?P<out_label>\w+))?'
                            r'(?: +\((?P<vpn>(\S+))\))?$')
        p3_1 = re.compile(r'^(?P<in_label>\w+)\/(?P<out_label>\w+)'
                            r'(?: +\((?P<vpn>(\S+))\))?$')

        for line in out.splitlines():
            line = line.strip()

            # BGP routing table information for VRF default, address family IPv4 Unicast
            m = p1.match(line)
            if m:
                vrf = m.groupdict()['vrf']
                address_family = m.groupdict()['af'].lower()
                continue

            # BGP table version is 7, Local Router ID is 10.106.0.6
            # BGP table version is 3, local router ID is 10.234.1.0
            m = p2.match(line)
            if m:
                if 'vrf' not in ret_dict:
                    ret_dict['vrf'] = {}
                if vrf not in ret_dict['vrf']:
                    ret_dict['vrf'][vrf] = {}
                if 'address_family' not in ret_dict['vrf'][vrf]:
                    ret_dict['vrf'][vrf]['address_family'] = {}
                if address_family not in ret_dict['vrf'][vrf]['address_family']:
                    ret_dict['vrf'][vrf]['address_family'][address_family] = {}

                sub_dict = ret_dict['vrf'][vrf]['address_family'][address_family]

                sub_dict['table_version'] = int(m.groupdict()['ver'])
                sub_dict['router_id'] = m.groupdict()['router_id']
                continue

            # Route Distinguisher: 10.234.1.0:3    (VRF vrf-9100)
            m = p4.match(line)
            if m:
                rd = m.groupdict()['rd']
                if 'vrf' not in ret_dict:
                    ret_dict['vrf'] = {}
                if vrf not in ret_dict['vrf']:
                    ret_dict['vrf'][vrf] = {}
                if 'address_family' not in ret_dict['vrf'][vrf]:
                    ret_dict['vrf'][vrf]['address_family'] = {}
                if address_family not in ret_dict['vrf'][vrf]['address_family']:
                    ret_dict['vrf'][vrf]['address_family'][address_family] = {}
                if 'route_distinguisher' not in ret_dict['vrf'][vrf]\
                    ['address_family'][address_family]:
                    ret_dict['vrf'][vrf]['address_family'][address_family]\
                        ['route_distinguisher'] = {}
                if rd not in ret_dict['vrf'][vrf]\
                    ['address_family'][address_family]['route_distinguisher']:
                    ret_dict['vrf'][vrf]['address_family'][address_family]\
                        ['route_distinguisher'][rd] = {}

                sub_dict = ret_dict['vrf'][vrf]['address_family']\
                    [address_family]['route_distinguisher'][rd]

                sub_dict['rd_vrf'] = m.groupdict()['vrf']
                continue


            # *>i10.36.210.0/24       10.106.101.1          nolabel/nolabel
            # * i0.0.0.0/0          10.36.1.0            nolabel/9100
            # *>i                   10.121.1.0            nolabel/9100
            # a10.4.0.0/16        0.0.0.0             nolabel/nolabel
            # *>e10.85.0.0/24        10.76.1.101          492288/nolabel (VRF1)
            # *>2001:db8:2913::/112           ::ffff:10.51.1.101
            m = p3.match(line)
            if m:
                prefix_cur = m.groupdict()['prefix']
                if prefix_cur:
                    index = 0
                    prefix = prefix_cur
                else:
                    index += 1

                status_code = m.groupdict()['status']
                best_code = m.groupdict()['best']
                type_code = m.groupdict()['type_code']
                next_hop = m.groupdict()['next_hop']
                in_label = m.groupdict()['in_label']
                out_label = m.groupdict()['out_label']
                vpn = m.groupdict()['vpn']


                if 'prefix' not in sub_dict:
                    sub_dict['prefix'] = {}
                if prefix not in sub_dict['prefix']:
                    sub_dict['prefix'][prefix] = {}
                if 'index' not in sub_dict['prefix'][prefix]:
                    sub_dict['prefix'][prefix]['index'] = {}
                if index not in sub_dict['prefix'][prefix]['index']:
                    sub_dict['prefix'][prefix]['index'][index] = {}

                if status_code:
                    sub_dict['prefix'][prefix]['index'][index]['status'] = \
                        status_map[status_code]
                    sub_dict['prefix'][prefix]['index'][index]['status_code'] = status_code
                else:
                    sub_dict['prefix'][prefix]['index'][index]['status'] = 'invalid'

                if best_code:
                    sub_dict['prefix'][prefix]['index'][index]['best_code'] = best_code
                sub_dict['prefix'][prefix]['index'][index]['best_path'] = \
                    True if best_code else False

                sub_dict['prefix'][prefix]['index'][index]['type'] = \
                    path_type_map[type_code]
                sub_dict['prefix'][prefix]['index'][index]['type_code'] = type_code

                sub_dict['prefix'][prefix]['index'][index]['nexthop'] = next_hop

                sub_dict['prefix'][prefix]['index'][index]\
                    .setdefault('in_label', in_label) if in_label else None
                sub_dict['prefix'][prefix]['index'][index]\
                    .setdefault('out_label', out_label) if out_label else None
                sub_dict['prefix'][prefix]['index'][index]\
                    .setdefault('vpn', vpn) if vpn else None
                continue

            #                                           nolabel/16
            #                                           22/17 (VRF1)
            m = p3_1.match(line)
            if m:
                in_label = m.groupdict()['in_label']
                out_label = m.groupdict()['out_label']
                vpn = m.groupdict()['vpn']
                sub_dict['prefix'][prefix]['index'][index]\
                    .setdefault('in_label', in_label) if in_label else None
                sub_dict['prefix'][prefix]['index'][index]\
                    .setdefault('out_label', out_label) if out_label else None
                sub_dict['prefix'][prefix]['index'][index]\
                    .setdefault('vpn', vpn) if vpn else None
                continue

        return ret_dict

    def xml(self, address_family, vrf=''):
        assert address_family in ['ipv4 unicast', 'ipv4 multicast',
                                  'ipv6 unicast', 'ipv6 multicast',
                                  'vpnv4 unicast', 'vpnv6 unicast']


        if vrf:
            cmd = self.xml_command[0].format(address_family=address_family, vrf=vrf)
            cli_cmd = self.cli_command[0].format(address_family=address_family, vrf=vrf)
        else:
            cmd = self.xml_command[1].format(address_family=address_family)
            cli_cmd = self.cli_command[0].format(address_family=address_family)

        out = self.device.execute(cmd)

        etree_dict = {}

        # Remove junk characters returned by the device
        out = out.replace("]]>]]>", "")
        root = ET.fromstring(out)

        # top table root
        show_root = Common.retrieve_xml_child(root=root, key='show')
        # get xml namespace
        # {http://www.cisco.com/nxos:7.0.3.I7.1.:bgp}
        try:
            m = re.compile(r'(?P<name>\{[\S]+\})').match(show_root.tag)
            namespace = m.groupdict()['name']
        except Exception:
            return etree_dict

        # compare cli command
        Common.compose_compare_command(root=root, namespace=namespace,
                                       expect_command=cli_cmd)

        # find Vrf root
        root = Common.retrieve_xml_child(root=root, key='TABLE_vrf')

        if not root:
            return etree_dict

        # -----   loop vrf  -----
        for vrf_tree in root.findall('{}ROW_vrf'.format(namespace)):
            # vrf
            try:
                vrf = vrf_tree.find('{}vrf-name-out'.format(namespace)).text
            except Exception:
                break

            # Address family table
            af_tree = vrf_tree.find('{}TABLE_afi'.format(namespace))
            if not af_tree:
                continue
            for af_root in af_tree.findall('{}ROW_afi'.format(namespace)):
                # Address family table
                saf_tree = af_root.find('{}TABLE_safi'.format(namespace))
                if not saf_tree:
                    continue
                # -----   loop address_family  -----
                for saf_root in saf_tree.findall('{}ROW_safi'.format(namespace)):
                    # neighbor
                    try:
                        af = saf_root.find('{}af-name'.format(namespace)).text
                        af = af.lower()
                    except Exception:
                        continue

                    # <table-version>7</table-version>
                    try:
                        table_version = \
                            int(saf_root.find('{}table-version'.format(namespace)).text)
                    except Exception:
                        table_version = None

                    # <router-id>10.106.0.6</router-id>
                    try:
                        router_id = \
                            saf_root.find('{}router-id'.format(namespace)).text
                    except Exception:
                        router_id = None

                    if table_version or router_id:
                        if 'vrf' not in etree_dict:
                            etree_dict['vrf'] = {}
                        if vrf not in etree_dict['vrf']:
                            etree_dict['vrf'][vrf] = {}

                        if 'address_family' not in etree_dict['vrf'][vrf]:
                            etree_dict['vrf'][vrf]['address_family'] = {}

                        if af not in etree_dict['vrf'][vrf]['address_family']:
                            etree_dict['vrf'][vrf]['address_family'][af] = {}
                        if table_version:
                            etree_dict['vrf'][vrf]['address_family'][af]['table_version'] = table_version
                        if router_id:
                            etree_dict['vrf'][vrf]['address_family'][af]['router_id'] = router_id

                     # RD table
                    rd_tree = saf_root.find('{}TABLE_rd'.format(namespace))
                    if not rd_tree:
                        continue

                    # -----   loop rd  -----
                    for rd_root in rd_tree.findall('{}ROW_rd'.format(namespace)):
                        # neighbor
                        try:
                            rd = rd_root.find('{}rd_val'.format(namespace)).text
                        except Exception:
                            rd = None

                        if rd:
                            if 'route_distinguisher' not in etree_dict['vrf'][vrf]:
                                etree_dict['vrf'][vrf]['address_family'][af]\
                                    ['route_distinguisher'] = {}

                            if rd not in etree_dict['vrf'][vrf]['address_family']:
                                etree_dict['vrf'][vrf]['address_family'][af]\
                                    ['route_distinguisher'][rd] = {}
                            sub_dict = etree_dict['vrf'][vrf]['address_family'][af]\
                                    ['route_distinguisher'][rd]
                        else:
                            sub_dict = etree_dict['vrf'][vrf]['address_family'][af]

                        # <rd_vrf>vrf-9100</rd_vrf>
                        try:
                            sub_dict['rd_vrf'] = rd_root.find('{}rd_vrf'.format(namespace)).text
                        except Exception:
                            pass

                         # prefix table
                        prefix_tree = rd_root.find('{}TABLE_prefix'.format(namespace))
                        if not prefix_tree:
                            continue

                        # -----   loop prefix  -----
                        for prefix_root in prefix_tree.findall('{}ROW_prefix'.format(namespace)):
                            # <ipprefix>10.1.1.1</ipprefix>
                            try:
                                prefix = prefix_root.find('{}ipprefix'.format(namespace)).text
                            except Exception:
                                # <ipv6prefix>2001:db8:4309::/112</ipv6prefix>
                                try:
                                    prefix = prefix_root.find('{}ipv6prefix'.format(namespace)).text
                                except Exception:
                                    continue 

                            if 'prefix' not in sub_dict:
                                sub_dict['prefix'] = {}

                            if prefix not in sub_dict['prefix']:
                                sub_dict['prefix'][prefix] = {}

                             # path table
                            index_tree = prefix_root.find('{}TABLE_path'.format(namespace))
                            if not index_tree:
                                continue

                            # -----   loop path  -----
                            for index_root in index_tree.findall('{}ROW_path'.format(namespace)):
                                # neighbor
                                try:
                                    index = int(index_root.find('{}pathnr'.format(namespace)).text)
                                except Exception:
                                    continue

                                if 'index' not in sub_dict['prefix'][prefix]:
                                    sub_dict['prefix'][prefix]['index'] = {}

                                if index not in sub_dict['prefix'][prefix]['index']:
                                    sub_dict['prefix'][prefix]['index'][index] = {}

                                # <status>valid</status>
                                sub_dict['prefix'][prefix]['index'][index]['status'] = \
                                    index_root.find('{}status'.format(namespace)).text

                                # <best>bestpath</best>
                                sub_dict['prefix'][prefix]['index'][index]['best_path'] = \
                                    False if 'none' in index_root.find('{}best'.format(namespace)).text \
                                    else True

                                # <type>internal</type>
                                sub_dict['prefix'][prefix]['index'][index]['type'] = \
                                    index_root.find('{}type'.format(namespace)).text

                                try:
                                    # <statuscode>*</statuscode>
                                    status_code = index_root.find('{}statuscode'.format(namespace)).text
                                    sub_dict['prefix'][prefix]['index'][index]\
                                        .setdefault('status_code', status_code) if status_code.strip() else None                                        

                                    # <bestcode>&gt;</bestcode>
                                    best_code = index_root.find('{}bestcode'.format(namespace)).text
                                    best_code = '>' if '&gt;' in best_code else best_code.strip()
                                    if best_code:
                                        sub_dict['prefix'][prefix]['index'][index]['best_code'] = best_code
                                       
                                    # <typecode>i</typecode>
                                    sub_dict['prefix'][prefix]['index'][index]['type_code'] = \
                                        index_root.find('{}typecode'.format(namespace)).text
                                except Exception:
                                    pass

                                # <ipnexthop>10.106.101.1</ipnexthop>
                                try:
                                    sub_dict['prefix'][prefix]['index'][index]['nexthop'] = \
                                        index_root.find('{}ipnexthop'.format(namespace)).text
                                except Exception:
                                    # <ipv6nexthop>2001:db8:1900:1::1:101</ipv6nexthop>
                                    try:
                                        sub_dict['prefix'][prefix]['index'][index]['nexthop'] = \
                                            index_root.find('{}ipv6nexthop'.format(namespace)).text
                                    except Exception:
                                        pass

                                # <inlabel>nolabel</inlabel>
                                sub_dict['prefix'][prefix]['index'][index]['in_label'] = \
                                    index_root.find('{}inlabel'.format(namespace)).text

                                # <outlabel>nolabel</outlabel>
                                sub_dict['prefix'][prefix]['index'][index]['out_label'] = \
                                    index_root.find('{}outlabel'.format(namespace)).text

                                # <vpn></vpn>
                                vpn = index_root.find('{}vpn'.format(namespace)).text
                                if vpn:
                                    sub_dict['prefix'][prefix]['index'][index]['vpn'] = vpn
                                    

                                # <hold_down></hold_down>
                                hold_down = index_root.find('{}hold_down'.format(namespace)).text
                                if hold_down:
                                    sub_dict['prefix'][prefix]['index'][index]['hold_down'] = hold_down

        return etree_dict

# ====================================================
#  schema for show bgp l2vpn evpn summary
# ====================================================
class ShowBgpL2vpnEvpnSummarySchema(MetaParser):
    """Schema for:
        show bgp l2vpn evpn summary"""

    schema = {
        'instance': {
            Any(): {
                'vrf': {
                    Any(): { 
                        'vrf_name_out': str, 
                        'vrf_router_id': str,
                        'vrf_local_as': int, 
                        'address_family': {
                            Any(): { 
                                'tableversion': int, 
                                'configuredpeers': int, 
                                'capablepeers': int, 
                                'totalnetworks': int, 
                                'totalpaths': int, 
                                'memoryused': int, 
                                'numberattrs': int,
                                'bytesattrs': int, 
                                'numberpaths': int,
                                'bytespaths': int, 
                                'numbercommunities': int, 
                                'bytescommunities': int,
                                'numberclusterlist': int, 
                                'bytesclusterlist': int, 
                                'dampening': str, 
                                'neighbor': {
                                    Any(): {
                                        'neighbor': str, 
                                        'version': int, 
                                        'msgrecvd': int, 
                                        'msgsent': int, 
                                        'neighbortableversion': int, 
                                        'inq': int, 
                                        'outq': int, 
                                        'remoteas': int, 
                                        'time': str, 
                                        'state': str,
                                        Optional('prefixreceived'): int,
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

# ====================================================
#  Parser for show bgp l2vpn evpn summary
# ====================================================
class ShowBgpL2vpnEvpnSummary(ShowBgpL2vpnEvpnSummarySchema):
    """parser for:
        show bgp l2vpn evpn summary"""

    cli_command = 'show bgp l2vpn evpn summary'
    exclude = [
      'msgrecvd',
      'msgsent', 
      'neighbortableversion',
      'time',
      'tableversion',
      'bytesclusterlist',
      'numberclusterlist',
      'bytesattrs',
      'memoryused',
      'numberattrs',
      'totalnetworks',
      'totalpaths',
      'prefixreceived',
      'capablepeers']

    def cli(self,output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        result_dict = {}
        # BGP summary information for VRF default, address family L2VPN EVPN
        # BGP router identifier 192.168.4.11, local AS number 100
        # BGP table version is 155, L2VPN EVPN config peers 2, capable peers 2
        # 32 network entries and 32 paths using 5708 bytes of memory
        # BGP attribute entries [20/3200], BGP AS path entries [0/0]
        # BGP community entries [1/32], BGP clusterlist entries [3/12]
        #
        # Neighbor        V    AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
        # 172.16.205.8    4   200     130     139      155    0    0 02:05:01 0
        # 90:90:90::3     4   500     200     300      400    0    0 03:52:17 0

        # Neighbor        V    AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
        # 1.1.1.1   4 4444444444
        #                         121842  120925     5549    0    0    11w6d 142       
        # 1.1.1.2   4 4444444444
        #                         118316  117369     5549    0    0     3w4d 142  

        p1 = re.compile(r'^\s*BGP +summary +information +for +VRF +(?P<vrf_name_out>[\w]+),'
                        r' +address +family +(?P<af_name>[\w\s]+)$')
        p2 = re.compile(
            r'^\s*BGP +router +identifier +(?P<vrf_router_id>[\d\.]+), +local +AS +number +(?P<vrf_local_as>[\d]+)$')
        p3 = re.compile(r'^\s*BGP +table +version +is +(?P<tableversion>[\d]+), +(?P<af_name>[\w\s]+)'
                        r' +config +peers +(?P<configuredpeers>[\d]+),'
                        r' +capable +peers +(?P<capablepeers>[\d]+)$')
        p4 = re.compile(
            r'^\s*(?P<totalnetworks>[\d]+) +network +entries +and +(?P<totalpaths>[\d]+) +paths +using'
            r' +(?P<memoryused>[\d]+) +bytes +of +memory$')
        p5 = re.compile(r'^\s*BGP +attribute +entries +\[(?P<numberattrs>[\d]+)\/(?P<bytesattrs>[\d]+)\],'
                        r' +BGP +AS +path +entries +\[(?P<numberpaths>[\d]+)\/(?P<bytespaths>[\d]+)\]$')

        p6 = re.compile(r'^\s*BGP +community +entries +\[(?P<numbercommunities>[\d]+)\/(?P<bytescommunities>[\d]+)\],'
                        r' +BGP +clusterlist +entries +\[(?P<numberclusterlist>[\d]+)\/(?P<bytesclusterlist>[\d]+)\]$')

        p7 = re.compile(
            r'^\s*(?P<neighborid>[\w\.\:]+) +(?P<neighborversion>[\d]+) +(?P<neighboras>[\d]+) +(?P<msgrecvd>[\d]+)'
            r' +(?P<msgsent>[\d]+) +(?P<neighbortableversion>[\d]+) +(?P<inq>[\d]+) +(?P<outq>[\d]+)'
            r' +(?P<time>[\w\:]+) +(?P<prefixreceived>[\w\s\)\(]+)$')
        
        p8a = re.compile(
            r'^\s*(?P<neighborid>[\w\.\:]+) +(?P<neighborversion>[\d]+) +((?P<neighboras>[\d]+)[\n]*)$')
        
        p8b = re.compile(
            r'^\s*((?P<msgrecvd>[\d]+)'
            r' +(?P<msgsent>[\d]+) +(?P<neighbortableversion>[\d]+) +(?P<inq>[\d]+) +(?P<outq>[\d]+)'
            r' +(?P<time>[\w\:]+) +(?P<prefixreceived>[\w\s\)\(]+))$')

        for line in out.splitlines():
            if line:
                line = line.rstrip()
            else:
                continue

            m = p1.match(line)
            if m:
                group = m.groupdict()
                instance = 'default'
                vrf_name_out = group.pop('vrf_name_out')
                bgp_dict = result_dict.setdefault('instance', {}).setdefault(instance, {}).\
                                       setdefault('vrf', {}).setdefault(vrf_name_out,{})
                bgp_dict.update({'vrf_name_out': vrf_name_out})
                af_name = group.pop('af_name').lower()
                af_dict = bgp_dict.setdefault('address_family',{}).setdefault(af_name,{})
                continue

            m = p2.match(line)
            if m:
                group = m.groupdict()
                bgp_dict.update({'vrf_router_id': group.pop('vrf_router_id')})
                bgp_dict.update({'vrf_local_as': int(group.pop('vrf_local_as'))})
                continue

            m = p3.match(line)
            if m:
                group = m.groupdict()
                af_dict.update({'tableversion':int(group.pop('tableversion'))})
                af_dict.update({'configuredpeers':int(group.pop('configuredpeers'))})
                af_dict.update({'capablepeers':int(group.pop('capablepeers'))})
                continue

            m1 = ""
            if p4.match(line):
                m1 = p4.match(line)
            if p5.match(line):
                m1 = p5.match(line)
            if p6.match(line):
                m1 = p6.match(line)
            if m1:
                group = m1.groupdict()
                try:
                    af_dict.update({k: int(v) for k, v in group.items()})
                except:
                    af_dict.update({k:v.lower() for k, v in group.items()})
                af_dict.update({'dampening':'disabled'})
                continue

            m = p7.match(line)
            if m:
                group = m.groupdict()
                neighborid = group.pop('neighborid')
                neighbor_dict = af_dict.setdefault('neighbor',{}).setdefault(neighborid, {})

                neighbor_dict.update({'neighbor':neighborid})
                neighbor_dict.update({'remoteas': int(group.pop('neighboras'))})
                neighbor_dict.update({'version': int(group.pop('neighborversion'))})
                neighbor_dict.update({'msgrecvd': int(group.pop('msgrecvd'))})
                neighbor_dict.update({'msgsent': int(group.pop('msgsent'))})
                neighbor_dict.update({'neighbortableversion': int(group.pop('neighbortableversion'))})
                neighbor_dict.update({'inq': int(group.pop('inq'))})
                neighbor_dict.update({'outq': int(group.pop('outq'))})
                neighbor_dict.update({'time': group.pop('time')})
                prefixreceived = group.pop('prefixreceived')
                try:
                    neighbor_dict.update({'prefixreceived': int(prefixreceived)})
                    neighbor_dict.update({'state': 'established'})
                except ValueError:
                    neighbor_dict.update({'state': prefixreceived.lower()})
                continue

            m = p8a.match(line)
            if m:
                group = m.groupdict()
                neighborid = group.pop('neighborid')
                neighbor_dict = af_dict.setdefault('neighbor',{}).setdefault(neighborid, {})

                neighbor_dict.update({'neighbor':neighborid})
                neighbor_dict.update({'remoteas': int(group.pop('neighboras'))})
                neighbor_dict.update({'version': int(group.pop('neighborversion'))})
                continue

            m = p8b.match(line)
            if m:
                group = m.groupdict()
                neighbor_dict.update({'msgrecvd': int(group.pop('msgrecvd'))})
                neighbor_dict.update({'msgsent': int(group.pop('msgsent'))})
                neighbor_dict.update({'neighbortableversion': int(group.pop('neighbortableversion'))})
                neighbor_dict.update({'inq': int(group.pop('inq'))})
                neighbor_dict.update({'outq': int(group.pop('outq'))})
                neighbor_dict.update({'time': group.pop('time')})
                prefixreceived = group.pop('prefixreceived')
                try:
                    neighbor_dict.update({'prefixreceived': int(prefixreceived)})
                    neighbor_dict.update({'state': 'established'})
                except ValueError:
                    neighbor_dict.update({'state': prefixreceived.lower()})
                continue


        return result_dict

# ==================================================================
#  schema for show bgp l2vpn evpn route-type <route_type> vrf <vrf>
# ==================================================================
class ShowBgpL2vpnEvpnRouteTypeSchema(MetaParser):
    """Schema for:
        show bgp l2vpn evpn route-type <route-type>
        show bgp l2vpn evpn route-type <route-type> vrf <vrf>"""

    schema = {
        'instance': {
            Any():{
                'vrf': {
                    Any(): {
                        'address_family': {
                            Any(): {
                                'rd': {
                                    Any(): {
                                        Optional('rd'): str,
                                        Optional('rd_vrf'): str,
                                        Optional('rd_vniid'): int,
                                        'prefix': {
                                            Any(): {
                                                'nonipprefix': str,
                                                'prefixversion': int,
                                                Optional('totalpaths'): int,
                                                'bestpathnr': int,
                                                Optional('mpath'): str,
                                                Optional('on_newlist'): bool,
                                                Optional('on_xmitlist'): bool,
                                                Optional('suppressed'): bool,
                                                Optional('needsresync'): bool,
                                                Optional('locked'): bool,
                                                'path': {
                                                    Any(): {
                                                        Optional('pathnr'): int,
                                                        Optional('policyincomplete'): bool,
                                                        Optional('pathtype'): str,
                                                        'pathvalid': bool,
                                                        'pathbest': bool,
                                                        Optional('pathdeleted'): bool,
                                                        Optional('pathstaled'): bool,
                                                        Optional('pathhistory'): bool,
                                                        Optional('pathovermaxaslimit'): bool,
                                                        Optional('pathmultipath'): bool,
                                                        Optional('pathnolabeledrnh'): bool,
                                                        Optional('imported_from'): str,
                                                        Optional('gateway_ip'): str,
                                                        Optional('as_path'): str,
                                                        'ipnexthop': str,
                                                        'nexthopmetric': int,
                                                        'neighbor': str,
                                                        'neighborid': str,
                                                        Optional('inaccessible'): bool,
                                                        'origin': str,
                                                        'localpref': int,
                                                        'weight': int,
                                                        Optional('inlabel'): int,
                                                        Optional('extcommunity'): list,
                                                        Optional('advertisedto'): list,
                                                        Optional('originatorid'): str,
                                                        Optional('clusterlist'): list,
                                                        Optional('pmsi_tunnel_attribute'): {
                                                            Optional('flags'): str,
                                                            Optional('label'): str,
                                                            Optional('tunnel_type'): str,
                                                            Optional('tunnel_id'): str,

                                                        }
                                                    }
                                                }
                                             }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }


# ==================================================================
#  Parser for show bgp l2vpn evpn route-type <route_type> vrf <vrf>
# ==================================================================
class ShowBgpL2vpnEvpnRouteType(ShowBgpL2vpnEvpnRouteTypeSchema):
    """parser for:
        show bgp l2vpn evpn route-type <route_type>
        show bgp l2vpn evpn route-type <route_type> vrf <vrf>"""
    cli_command = ['show bgp l2vpn evpn route-type {route_type}', 'show bgp l2vpn evpn route-type {route_type} vrf {vrf}']
    exclude = [
      'prefixversion',
      'Extcommunity',
      'prefixversion']

    def cli(self,route_type,vrf='',output=None):
        if not route_type:
            out = ""
        if output is None:
            if vrf:
                out = self.device.execute(self.cli_command[1].format(route_type=route_type,vrf=vrf))
            else:
                out = self.device.execute(self.cli_command[0].format(route_type=route_type))
        else:
            out = output

        result_dict = {}

        # BGP routing table information for VRF default, address family L2VPN EVPN
        # Route Distinguisher: 10.121.0.55:27001   (ES [0300.00ff.0001.2c00.0309 0])
        # BGP routing table entry for [4]:[0300.00ff.0001.2c00.0309]:[32]:[192.168.111.55]/136, version 13144
        # Paths: (1 available, best #1)
        # Flags: (0x000002) (high32 00000000) on xmit-list, is not in l2rib/evpn
        # Multipath: iBGP
        #
        #   Advertised path-id 1
        #   Path type: local (0xcf9bdc54), path is valid, is best path, no labeled nexthop
        #   AS-Path: NONE, path locally originated
        #     192.168.111.55 (metric 0) from 0.0.0.0 (10.121.0.55)
        #       Origin IGP, MED not set, localpref 100, weight 32768
        #       Received label 25000
        #       Extcommunity: ENCAP:8 RT:0000.00ff.012c
        #
        #   Path-id 1 advertised to peers:
        #     10.121.0.11          10.121.0.22          10.121.0.33          10.121.0.44
        #     10.196.0.11

        p1 = re.compile(r'^\s*BGP +routing +table +information +for +VRF +(?P<vrf_name_out>[\w]+),'
                        r' +address +family +(?P<af_name>[\w\s]+)$')
        p2 = re.compile(r'^\s*Route Distinguisher: +(?P<rd>[\w\.\:]+)( +\(ES +(?P<es>[\w\s\[\]\.]+)\))?( +\((?P<rd_vrf>[\w]+)VNI +(?P<rd_vniid>[\d]+)\))?$')
        p3 = re.compile(r'^\s*BGP routing table entry for +(?P<nonipprefix>[\w\[\]\:\.\/]+), +version +(?P<prefixversion>[\d]+)$')
        p4 = re.compile(r'^\s*Paths: +\((?P<totalpaths>[\d]+) +available, +best +#(?P<bestpathnr>[\d]+)\)$')
        p5 = re.compile(r'^\s*Flags: (?P<flag_xmit>[\S\s]+) +on +xmit-list(, +(?P<flags_attr>[\w\s\/\,]+))?$')
        p6 = re.compile(r'^\s*Multipath: +(?P<multipath>[\w]+)$')
        p7 = re.compile(r'^\s*Advertised path-id +(?P<path_id>[\d]+)$')
        p8 = re.compile(r'^\s*Path type: +(?P<path_type>[\w\s\(\)]+), +(?P<pathtypes>[\S\s\,\:\/]+)?$')
        #          Imported from 99.99.99.99:10:[5]:[0]:[0]:[32]:[100.4.1.2]/224
        p9 = re.compile(r'^\s*Imported from +(?P<imported_from>[\w\.\:\/\[\]\,]+)$')
        #   Gateway IP: 0.0.0.0
        p10 = re.compile(r'^\s*Gateway IP: +(?P<gateway_ip>[a-zA-Z0-9\.\:]+)$')
        #   AS-Path: 4 1 10 33299 51178 47751 {27016} , path sourced external to AS
        p11 = re.compile(r'^\s*AS-Path: +(?P<as_path>[\d\s\{\}]+|[\w]+)(, +path locally originated)?(, +path sourced +(?P<internal_external>[\w]+) to AS)?$')
        p12 = re.compile(r'^\s*(?P<ipnexthop>[\d\.]+) +\((?:(?P<inaccessible>(inaccessible)), +)?metric +(?P<nexthopmetric>[\d]+)\) +from +(?P<neighbor>[\d\.]+)'
                         r' +\((?P<neighborid>[\d\.]+)\)$')
        p13 = re.compile(r'^\s*Origin +(?P<origin>[\w]+), +(MED +(?P<med>[\w\s]+),)? +localpref +(?P<localpref>[\d]+),'
                         r' +weight +(?P<weight>[\d]+)$')
        p14 = re.compile(r'^\s*Extcommunity: +(?P<extcommunity>[\w\s\:\.]+)$')
        p15 = re.compile(r'^\s*Originator: +(?P<originatorid>[\d\.]+) +Cluster +list: +(?P<clusterlist>[\d\.]+)$')
        p16 = re.compile(r'^\s*Path-id +(?P<path_id>[\d]+) +advertised to peers:$')
        p17 = re.compile(r'^\s*(?P<advertisedto>[\d\s\.]+)$')
        p18 = re.compile(r'^\s*Received +label +(?P<inlabel>[\d]+)$')

        # PMSI Tunnel Attribute:
        p19 = re.compile(r'^\s*(?P<attribute>[\w]+) +Tunnel +Attribute:$')
        #         flags: 0x00, Tunnel type: Ingress Replication
        p20 = re.compile(r'^\s*flags: +(?P<flags>[\w]+), +Tunnel type: +(?P<tunnel_type>[\w\s]+)$')
        #         Label: 10101, Tunnel Id: 10.196.7.7
        p21 = re.compile(r'^\s*Label: +(?P<label>[\d]+), +Tunnel +Id: +(?P<tunnel_id>[\d\.]+)$')

        for line in out.splitlines():
            if line:
                line = line.rstrip()
            else:
                continue

            m = p1.match(line)
            if m:
                group = m.groupdict()
                instance = 'default'
                vrf_name_out = group.pop('vrf_name_out')
                af_name = group.get('af_name').lower()
                continue

            m = p2.match(line)
            if m:
                group = m.groupdict()
                bgp_dict = result_dict.setdefault('instance', {}).setdefault(instance, {}).\
                                                setdefault('vrf', {}).setdefault(vrf_name_out, {})
                af_dict = bgp_dict.setdefault('address_family', {}).setdefault(af_name, {})
                rd = group.pop('rd')
                rd_dict = af_dict.setdefault('rd',{}).setdefault(rd,{})
                rd_dict.update({'rd':rd})
                if group.get('rd_vniid'):
                    rd_dict.update({'rd_vrf': group.pop('rd_vrf').lower()})
                    rd_dict.update({'rd_vniid': int(group.pop('rd_vniid'))})
                continue

            m = p3.match(line)
            if m:
                group = m.groupdict()
                nonipprefix = group.pop('nonipprefix').strip()
                prefix_dict = rd_dict.setdefault('prefix',{}).setdefault(nonipprefix,{})
                prefix_dict.update({'nonipprefix': nonipprefix})
                prefix_dict.update({'prefixversion': int(group.pop('prefixversion'))})
                index = 0
                continue

            m = p4.match(line)
            if m:
                group = m.groupdict()
                prefix_dict.update({k:int(v) for k,v in group.items()})
                continue

            m = p5.match(line)
            if m:
                prefix_dict.update({'on_xmitlist':True})
                continue

            m = p6.match(line)
            if m:
                group = m.groupdict()
                mpath  = group.pop('multipath').lower()
                prefix_dict.update({'mpath': mpath})
                continue


            m = p7.match(line)
            if m:
                group = m.groupdict()
                path_temp_dict = prefix_dict.setdefault('path',{})
                continue

            m = p8.match(line)
            if m:
                index += 1
                path_temp_dict = prefix_dict.setdefault('path', {})
                path_dict = path_temp_dict.setdefault(index, {})
                path_dict.update({'pathnr': index-1})
                group = m.groupdict()
                pathtype = group.get('path_type').strip()
                path_dict.update({'pathtype': pathtype})
                pathtypes = group.get('pathtypes')
                if 'path is valid' in pathtypes:
                    path_dict.update({'pathvalid': True})
                else:
                    path_dict.update({'pathvalid': False})

                if 'is best path' in pathtypes:
                    path_dict.update({'pathbest': True})
                else:
                    path_dict.update({'pathbest': False})
                if 'no labeled nexthop' in pathtypes:
                    path_dict.update({'pathnolabeledrnh': True})
                else:
                    path_dict.update({'pathnolabeledrnh': False})
                continue
            
            m = p9.match(line)
            if m:
                group = m.groupdict()
                path_dict.update({'imported_from': group.get('imported_from')})
                continue

            m = p10.match(line)
            if m:
                group = m.groupdict()
                path_dict.update({'gateway_ip': group.get('gateway_ip')})
                continue

            m = p11.match(line)
            if m:
                group = m.groupdict()
                as_path = group.get('as_path').strip().lower()
                path_dict.update({'as_path': as_path})	
                continue

            m = p12.match(line)
            if m:
                group = m.groupdict()
                path_dict['ipnexthop'] = group['ipnexthop']
                path_dict['nexthopmetric'] = int(group['nexthopmetric'])
                path_dict['neighbor'] = group['neighbor']
                path_dict['neighborid'] = group['neighborid']
                if group['inaccessible']:
                    path_dict['inaccessible'] = True
                continue

            m = p13.match(line)
            if m:
                group = m.groupdict()
                path_dict.update({'origin': group.pop('origin').lower()})
                path_dict.update({'localpref': int(group.pop('localpref'))})
                path_dict.update({'weight': int(group.pop('weight'))})
                continue

            m = p14.match(line)
            if m:
                group = m.groupdict()
                path_dict.update({k: v.split( ) for k, v in group.items()})
                continue

            m = p15.match(line)
            if m:
                group = m.groupdict()
                path_dict.update({'originatorid': group.pop('originatorid')})
                path_dict.update({'clusterlist': group.pop('clusterlist').split()})
                continue


            m = p17.match(line)
            if m:
                group = m.groupdict()
                for k, v in group.items():
                    if k in path_dict:
                        path_dict[k].append(v)
                    else:
                        path_dict.update({k:v.split()})
                continue

            m = p18.match(line)
            if m:
                group = m.groupdict()
                path_dict.update({'inlabel': int(group.pop('inlabel'))})
                continue

            m = p19.match(line)
            if m:
                group = m.groupdict()
                tunnel_dict = path_dict.setdefault('pmsi_tunnel_attribute',{})
                continue

            m = p20.match(line)
            if m:
                group = m.groupdict()
                tunnel_dict.update({k:v for k, v in group.items()})
                continue

            m = p21.match(line)
            if m:
                group = m.groupdict()
                tunnel_dict.update({k: v for k, v in group.items()})
                continue

        if 'instance' not in result_dict:
            return result_dict

        for instance in result_dict['instance']:
            if 'vrf' not in result_dict['instance'][instance]:
                continue
            for vrf in result_dict['instance'][instance]['vrf']:
                vrf_dict = result_dict['instance'][instance]['vrf'][vrf]
                if 'address_family' not in vrf_dict:
                    continue
                for af in vrf_dict['address_family']:
                    af_dict = vrf_dict['address_family'][af]
                    if 'rd' not in af_dict:
                        continue
                    for rd in af_dict['rd']:
                        if 'prefix' not in af_dict['rd'][rd]:
                            continue
                        for prefix in af_dict['rd'][rd]['prefix']:
                            if 'path' not in af_dict['rd'][rd]['prefix'][prefix]:
                                continue
                            for index in af_dict['rd'][rd]['prefix'][prefix]['path']:
                                if len(af_dict['rd'][rd]['prefix'][prefix]['path'][index].keys()) > 1:
                                    ind = 1
                                    next_dict = {}
                                    sorted_list = sorted(af_dict['rd'][rd]['prefix'][prefix]['path'].items(),
                                                         key=lambda x: x[1]['neighbor'])
                                    for i, j in enumerate(sorted_list):
                                        next_dict[ind] = af_dict['rd'][rd]['prefix'][prefix]['path'][j[0]]
                                        ind += 1
                                    del (af_dict['rd'][rd]['prefix'][prefix]['path'])
                                    af_dict['rd'][rd]['prefix'][prefix]['path'] = next_dict


        return result_dict

# ==========================================================
#  schema for show bgp l2vpn evpn neighbors
# ===========================================================
class ShowBgpL2vpnEvpnNeighborsSchema(MetaParser):
    """Schema for:
        show bgp l2vpn evpn neighbors"""


    schema = {
        'instance': {
            Any(): {
                'vrf': {
                    Any(): { 
                        'address_family': {
                            Any(): { 
                                'neighbor': {
                                    Any(): {
                                        'neighbor': str, 
                                        'remoteas': int, 
                                        Optional('localas'): int,
                                        Optional('link'): str,
                                        Optional('index'): int,
                                        Optional('version'): int,
                                        Optional('remote_id'): str,
                                        Optional('state'): str,
                                        Optional('up'): bool,
                                        Optional('retry'): str,
                                        Optional('elapsedtime'): str,
                                        Optional('connectedif'): str,
                                        Optional('bfd'): bool,
                                        Optional('ttlsecurity'): bool, 
                                        Optional('password'): bool,
                                        Optional('passiveonly'): bool,
                                        Optional('localas_inactive'): bool,
                                        Optional('remote_privateas'): bool,
                                        'lastread': str, 
                                        'holdtime': int, 
                                        'keepalivetime': int, 
                                        Optional('lastwrite'): str,
                                        Optional('keepalive'): str,
                                        'msgrecvd': int, 
                                        'notificationsrcvd': int,
                                        'recvbufbytes': int, 
                                        'msgsent': int, 
                                        'notificationssent': int, 
                                        'sentbytesoutstanding': int,
                                        Optional('totalbytessent'): int, 
                                        'connsestablished': int,
                                        'connsdropped': int, 
                                        Optional('resettime'): str,
                                        Optional('resetreason'): str, 
                                        Optional('peerresettime'): str, 
                                        Optional('peerresetreason'): str,
                                        Optional('capsnegotiated'): bool,
                                        Optional('capmpadvertised'): bool,
                                        Optional('caprefreshadvertised'): bool,
                                        Optional('capgrdynamicadvertised'): bool,
                                        Optional('capmprecvd'): bool,
                                        Optional('caprefreshrecvd'): bool,
                                        Optional('capgrdynamicrecvd'): bool,
                                        Optional('capolddynamicadvertised'): bool,
                                        Optional('capolddynamicrecvd'): bool,
                                        Optional('caprradvertised'): bool,
                                        Optional('caprrrecvd'): bool,
                                        Optional('capoldrradvertised'): bool,
                                        Optional('capoldrrrecvd'): bool,
                                        Optional('capas4advertised'): bool,
                                        Optional('capas4recvd'): bool,
                                        Optional('af'): {
                                            Any(): { 
                                                'af_advertised': bool, 
                                                'af_recvd': bool, 
                                                'af_name': str, 
                                            }
                                        },
                                        Optional('capgradvertised'): bool,
                                        Optional('capgrrecvd'): bool,
                                        Optional('graf'): {
                                            Any(): { 
                                                Optional('gr_af_name'): str,
                                                Optional('gr_adv'): bool,
                                                Optional('gr_recv'): bool,
                                                Optional('gr_fwd'): bool,
                                            }
                                        },
                                        Optional('grrestarttime'): int,
                                        Optional('grstaletiem'): int,
                                        Optional('grrecvdrestarttime'): int,
                                        Optional('capextendednhadvertised'): bool,
                                        Optional('capextendednhrecvd'): bool,
                                        Optional('capextendednhaf'): {
                                            Any(): { 
                                                Optional('capextendednh_af_name'): str,
                                            }
                                        },
                                        Optional('epe'): bool, 
                                        Optional('firstkeepalive'): bool, 
                                        'openssent': int, 
                                        'opensrecvd': int, 
                                        'updatessent': int,
                                        'updatesrecvd': int, 
                                        'keepalivesent': int, 
                                        'keepaliverecvd': int,
                                        'rtrefreshsent': int, 
                                        'rtrefreshrecvd': int,
                                        'capabilitiessent': int, 
                                        'capabilitiesrecvd': int,
                                        'bytessent': int,
                                        'bytesrecvd': int,
                                        Optional('peraf'): {
                                            Any(): { 
                                                Optional('per_af_name'): str,
                                                Optional('tableversion'): int,
                                                Optional('neighbortableversion'): int,
                                                Optional('pfxrecvd'): int,
                                                Optional('pfxbytes'): int,
                                                Optional('insoftreconfigallowed'): bool, 
                                                Optional('sendcommunity'): bool, 
                                                Optional('sendextcommunity'): bool, 
                                                Optional('asoverride'): bool, 
                                                Optional('peerascheckdisabled'): bool, 
                                                Optional('rrconfigured'): bool, 
                                                Optional('pfxbytes'): int, 

                                            }
                                        },
                                        Optional('localaddr'): str,
                                        Optional('localport'): int,
                                        Optional('remoteaddr'): str,
                                        Optional('remoteport'): int,
                                        Optional('fd'): int,
                                        Optional('enhanced_error_processing'): {
                                            Optional('error_processing'): bool,
                                            Optional('discarded_attr'): int,
                                        },
                                        Optional('last_error_length_sent'): int,
                                        Optional('reset_error_value_sent'): int,
                                        Optional('reset_error_sent_major'): int,
                                        Optional('reset_error_sent_minor'): int,
                                        Optional('last_error_length_received'): int,
                                        Optional('reset_error_value_received'): int,
                                        Optional('reset_error_received_major'): int,
                                        Optional('reset_error_received_minor'): int,
                                        Optional('accepted_prefixes'): int,
                                        Optional('memory_consumed_in_bytes'): int,
                                        Optional('received_prefixes'): int,
                                        Optional('sent_prefixes'): int,
                                        Optional('advertise_gw_ip'): bool,
                                        Optional('outbound_route_map'): str,
                                        Optional('last_end_of_rib_sent'): str,
                                        Optional('last_end_of_rib_received'): str,
                                        Optional('first_convergence'): str,
                                        Optional('convergence_routes_sent'): int,
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

# ====================================================
#  Parser for show bgp l2vpn evpn neighbors
# ====================================================
class ShowBgpL2vpnEvpnNeighbors(ShowBgpL2vpnEvpnNeighborsSchema):
    """parser for:
        show bgp l2vpn evpn neighbors"""

    cli_command = 'show bgp l2vpn evpn neighbors'
    exclude = [
      'bytesrecvd',
      'bytessent',
      'connsdropped',
      'connsestablished',
      'elapsedtime',
      'keepalive',
      'keepaliverecvd',
      'keepalivesent',
      'lastread',
      'lastwrite',
      'localport',
      'msgrecvd',
      'msgsent',
      'notificationssent',
      'opensrecvd',
      'openssent',
      'neighbortableversion',
      'tableversion',
      'updatesrecvd',
      'updatessent',
      'fd',
      'capabilitiesrecvd',
      'capabilitiessent',
      'remoteport',
      'resetreason',
      'resettime',
      'rtrefreshsent',
      'rtrefreshrecvd',
      'retry']

    def cli(self,output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output
        result_dict = {}
        recieve_flag = gr_adv_flag = gr_recv_flag = gr_fwd_flag = gr_flag = False
        # BGP neighbor is 172.16.205.8, remote AS 200, ebgp link, Peer index 3
        # BGP version 4, remote router ID 192.168.144.33
        # BGP state = Idle, down for 4w6d, retry in 0.000000
        # BGP state = Shut (Admin), down for 5w0d
        # BGP state = Established, up for 02:11:53
        # Peer is directly attached, interface Ethernet1/6
        # Enable logging neighbor events
        # BFD live-detection is configured and enabled, state is Invalid
        # TCP MD5 authentication is set (enabled)
        # Last read 00:00:51, hold time = 180, keepalive interval is 60 seconds
        # Last written 00:00:21, keepalive timer expiry due 00:00:38
        # Received 137 messages, 0 notifications, 0 bytes in queue
        # Sent 146 messages, 0 notifications, 0(0) bytes in queue
        # Connections established 1, dropped 0
        # Last reset by us never, due to No error
        # Last reset by peer never, due to No error
        #
        # Neighbor capabilities:
        # Dynamic capability: advertised (mp, refresh, gr) received (mp, refresh, gr)
        # Dynamic capability (old): advertised received
        # Route refresh capability (new): advertised received
        # Route refresh capability (old): advertised received
        # 4-Byte AS capability: advertised received
        # Address family L2VPN EVPN: advertised received
        # Graceful Restart capability: advertised received
        #
        # Graceful Restart Parameters:
        # Address families advertised to peer:
        #   L2VPN EVPN
        # Address families received from peer:
        #   L2VPN EVPN
        # Forwarding state preserved by peer for:
        # Restart time advertised to peer: 120 seconds
        # Stale time for routes advertised by peer: 300 seconds
        # Restart time advertised by peer: 120 seconds
        # Extended Next Hop Encoding Capability: advertised received
        # Receive IPv6 next hop encoding Capability for AF:
        #   IPv4 Unicast
        #
        # Message statistics:
        #                             Sent               Rcvd
        # Opens:                         1                  1
        # Notifications:                 0                  0
        # Updates:                      70                  1
        # Keepalives:                  129                133
        # Route Refresh:                 0                  0
        # Capability:                    2                  2
        # Total:                       146                137
        # Total bytes:               10398               2595
        # Bytes in queue:                0                  0
        #
        # For address family: L2VPN EVPN
        # BGP table version 191, neighbor version 191
        # 0 accepted paths consume 0 bytes of memory
        # Community attribute sent to this neighbor
        # Extended community attribute sent to this neighbor
        # Last End-of-RIB received 00:00:01 after session start
        # Last End-of-RIB sent 00:00:01 after session start
        # First convergence 00:00:01 after session start with 5 routes sent
        #
        # Local host: 172.16.205.6, Local port: 179
        # Foreign host: 172.16.205.8, Foreign port: 52715
        # fd = 84

        p1 = re.compile(r'^\s*BGP +neighbor +is +(?P<neighbor>[\d\.]+), remote AS +(?P<remoteas>[\d]+), +(?P<link>[\w]+) +link,'
                        r' +Peer index +(?P<index>[\d]+)$')
        p2 = re.compile(r'^\s*BGP version +(?P<version>[\d]+), remote router ID +(?P<remote_id>[\d\.]+)$')
        p3 = re.compile(r'^\s*BGP +state += +(?P<state>[\w\s\(\)]+), +(?P<up>[\w]+) +for'
                        r' +(?P<elapsedtime>[\w\:]+)(, +retry in +(?P<retry>[\w\:]+))?$')
        p4 = re.compile(r'^\s*Peer is directly attached, interface +(?P<connectedif>[\w\/]+)$')
        p5 = re.compile(r'^\s*BFD live-detection is configured and enabled, state is +(?P<bfd_state>[\w]+)?$')
        p6 = re.compile(r'^\s*TCP MD5 authentication is set \(enabled\)$')
        p7 = re.compile(r'^\s*Last read +(?P<lastread>[\w\:\.]+), hold time = +(?P<holdtime>[\d]+),'
                            r' +keepalive interval is +(?P<keepalivetime>[\d]+) +seconds$')
        p8 = re.compile(r'^\s*Last written +(?P<lastwrite>[\w\:\.]+), keepalive timer expiry due +(?P<keepalive>[\w\:]+)$')
        p9 = re.compile(r'^\s*Received +(?P<msgrecvd>[\d]+) +messages, +(?P<notificationsrcvd>[\d]+) +notifications,'
                        r' +(?P<recvbufbytes>[\d]+)+ bytes in queue$')
        p10 = re.compile(r'^\s*Sent +(?P<msgsent>[\d]+) messages,'
                          r' +(?P<notificationssent>[\d]+)'
                          r' +notifications, +(?P<sentbytesoutstanding>[\d]+)'
                          r'(?:\((?P<totalbytessent>[\d]+)\))? +bytes in queue$')
        p11 = re.compile(r'^\s*Connections established +(?P<connsestablished>[\d]+), +dropped +(?P<connsdropped>[\d]+)$')
        p12 = re.compile(r'^\s*Last reset by us +(?P<resettime>[\w]+), +due to +(?P<resetreason>[\w\s]+)$')
        p13 = re.compile(r'^\s*Last reset by peer +(?P<peerresettime>[\w]+), due to +(?P<peerresetreason>[\w\s]+)$')
        p14 = re.compile(r'^\s*Dynamic capability: advertised +\(+(?P<cap_advertised>[\w\,\s]+)\) +received +\(+(?P<cap_received>[\w\,\s]+)\)$')
        p15 = re.compile(r'^\s*Dynamic capability \(old\): +(?P<capolddynamicadvertised>[\w]+)( +(?P<capolddynamicrecvd>[\w\s]+))?$')
        p16 = re.compile(r'^\s*Route refresh capability \(new\): +(?P<caprradvertised>[\w]+)( +(?P<caprrrecvd>[\w]+))?$')
        p17 = re.compile(r'^\s*Route refresh capability \(old\): +(?P<capoldrradvertised>[\w]+)( +(?P<capoldrrrecvd>[\w]+))?$')
        p18 = re.compile(r'^\s*4-Byte AS capability: +(?P<capas4advertised>[\w]+)( +(?P<capas4recvd>[\w]+))?$')
        p19 = re.compile(r'^\s*Address family +(?P<af_name>[\w\s]+): +(?P<af_advertised>[a][\w]+)( +(?P<af_recvd>[r][\w]+))?$')
        p20 = re.compile(r'^\s*Graceful Restart capability: +(?P<capgradvertised>[\w]+)( +(?P<capgrrecvd>[\w]+))?$')
        p20_1 = re.compile(r'^\s*Graceful Restart Parameters:$')
        p21 = re.compile(r'^\s*Address families advertised to peer:$')
        p22 = re.compile(r'^(?P<space>\s{4})((?P<gr_af_name>(?!Sent)[\w].*)+)$')
        p23 = re.compile(r'^\s*Address families received from peer:$')
        p24_1 = re.compile(r'^\s*Forwarding state preserved by peer for:$')
        p25 = re.compile(r'^\s*Restart time advertised to peer: +(?P<grrestarttime>[\d]+) +seconds$')
        p26 = re.compile(r'^\s*Stale time for routes advertised by peer: +(?P<grstaletiem>[\d]+) +seconds$')
        p27 = re.compile(r'^\s*Restart time advertised by peer: +(?P<grrecvdrestarttime>[\d]+) +seconds$')
        p28 = re.compile(r'^\s*Extended Next Hop Encoding Capability: +(?P<capextendednhadvertised>[\w]+)( +(?P<capextendednhrecvd>[\w]+))?$')
        p29 = re.compile(r'^\s*Receive IPv6 next hop encoding Capability for AF:$')
        p30 = re.compile(r'^\s*(?P<space>\s{4})(?P<capextendednh_af_name>[\w\s]+)$')
        p31 = re.compile(r'^\s*Opens: +(?P<openssent>[\d]+) +(?P<opensrecvd>[\d]+)$')
        p32 = re.compile(r'^\s*Notifications: +(?P<notificationssent>[\d]+) +(?P<notificationsrcvd>[\d]+)$')
        p33 = re.compile(r'^\s*Updates: +(?P<updatessent>[\d]+) +(?P<updatesrecvd>[\d]+)$')
        p34 = re.compile(r'^\s*Keepalives: +(?P<keepalivesent>[\d]+) +(?P<keepaliverecvd>[\d]+)$')
        p35 = re.compile(r'^\s*Route Refresh: +(?P<rtrefreshsent>[\d]+) +(?P<rtrefreshrecvd>[\d]+)$')
        p36 = re.compile(r'^\s*Capability: +(?P<capabilitiessent>[\d]+) +(?P<capabilitiesrecvd>[\d]+)$')
        p38 = re.compile(r'^\s*Total bytes: +(?P<bytessent>[\d]+) +(?P<bytesrecvd>[\d]+)$')
        p39 = re.compile(r'^\s*Bytes in queue: +(?P<bytesinqueuesent>[\d]+) +(?P<bytesinqueuerecvd>[\d]+)$')
        p40 = re.compile(r'^\s*For address family: +(?P<per_af_name>[\w\ ]+)$')
        p41 = re.compile(r'^\s*BGP table version +(?P<tableversion>[\d]+), neighbor version +(?P<neighbortableversion>[\d]+)$')
        p42 = re.compile(r'^\s*(?P<pfxrecvd>[\d]+) +accepted paths consume +(?P<pfxbytes>[\d]+) +bytes of memory$')
        p43 = re.compile(r'^\s*Community attribute sent to this neighbor$')
        p44 = re.compile(r'^\s*Extended community attribute sent to this neighbor$')
        p46 = re.compile(r'^\s*Last End-of-RIB received +(?P<lastendribreceived>[\w\:]+) +after session start$')
        p47 = re.compile(r'^\s*Last End-of-RIB sent +(?P<lastendribsent>[\w\:]+) +after session start$')
        p48 = re.compile(r'^\s*First convergence +(?P<rrconfigured>[\w\:]+)'
                         r' +after session start with +(?P<pfxbytes>[\d]+) +routes sent$')
        p49 = re.compile(r'^\s*Local host: +(?P<localaddr>[\d\.]+), Local port: +(?P<localport>[\d\.]+)$')
        p50 = re.compile(r'^\s*Foreign host: +(?P<remoteaddr>[\d\.]+), Foreign port: +(?P<remoteport>[\d]+)$')
        p51 = re.compile(r'^\s*fd = +(?P<fd>[\d]+)$')

        # Enhanced error processing: On
        p52 = re.compile(r'\s*Enhanced error processing\: +(?P<error_processing>\w+)$')

        # 0 discarded attributes
        p53 = re.compile(r'\s*(?P<discarded_attr>\d) +discarded +attributes$')
        
        # Last error length received: 0 
        p54 = re.compile(r'\s*Last +error +length +received\: +(?P<last_error_length_sent>\d+)$')
        
        # Reset error value sent: 0
        p55 = re.compile(r'\s*Reset +error +value +received(\:)? +(?P<reset_error_value_sent>\d+)$')

        # Reset error sent major: 0 minor: 0
        p56 = re.compile(r'\s*Reset +error +sent +major\: '
                        r'+(?P<reset_error_sent_major>\d+) +minor\: '
                        r'+(?P<reset_error_sent_minor>\d+)$')
        
        # Last error length received: 0
        p57 = re.compile(r'\s*Last +error +length +received\: +(?P<last_error_length_received>\d+)$')

        # Reset error value received 0
        p58 = re.compile(r'\s*Reset error value received(\:)? +(?P<reset_error_value_received>\d+)$')

        # Reset error received major: 0 minor: 0
        p59 = re.compile(r'\s*Reset error received major\: '
                        r'+(?P<reset_error_received_major>\d+) +minor\:'
                        r' +(?P<reset_error_received_minor>\d+)$')

        # 10 accepted prefixes (10 paths), consuming 2360 bytes of memory
        p60 = re.compile(r'\s*(?P<accepted_prefixes>\d+) +accepted prefixes'
                        r' +\(\d+ +paths\)\, +consuming '
                        r'+(?P<memory_consumed_in_bytes>\d+) +bytes +of +memory$')

        # 0 received prefixes treated as withdrawn
        p61 = re.compile(r'\s*(?P<received_prefixes>\d+) +received '
                        r'+prefixes +treated +as +withdrawn$')
        
        # 40541 sent prefixes (40541 paths)
        p62 = re.compile(r'\s*(?P<sent_prefixes>\d+) +sent prefixes +\(\d+ paths\)$')

        # Advertise GW IP is enabled
        p63 = re.compile(r'\s*Advertise +GW +IP +is +(?P<advertise_gw_ip>\w+)$')

        # Outbound route-map configured is GENIE_TEST, handle obtained
        p64 = re.compile(r'\s*Outbound +route\-map +configured +is '
                        r'+(?P<outbound_route_map>\w+)\, +handle +obtained$')

        # Last End-of-RIB received 00:00:11 after session start
        # Last End-of-RIB sent 00:00:06 after session start
        p65 = re.compile(r'\s*Last +End\-of\-RIB +(?P<action>received|sent) '
                        r'+(?P<time>[\w:]+) +after +session +start$')

        # First convergence 00:00:06 after session start with 18810 routes sent
        p66 = re.compile(r'\s*First +convergence +(?P<first_convergence>[\w:]+) '
                        r'+after +session +start +with '
                        r'+(?P<convergence_routes_sent>\d+) +routes +sent$')

        for line in out.splitlines():
            if line:
                line = line.rstrip()
            else:
                continue

            m = p1.match(line)
            if m:
                group = m.groupdict()
                instance = 'default'
                vrf_name = 'default'
                bgp_dict = result_dict.setdefault('instance', {}).setdefault(instance, {}).\
                                       setdefault('vrf', {}).setdefault(vrf_name,{})
                af_name = 'l2vpn evpn'
                af_dict = bgp_dict.setdefault('address_family',{}).setdefault(af_name,{})
                neighbor = group.get('neighbor')
                neighbor_dict = af_dict.setdefault('neighbor',{}).setdefault(neighbor,{})
                for k, v in group.items():
                    if v.isdigit():
                        neighbor_dict.update({k:int(v)})
                    else:
                        neighbor_dict.update({k:v})
                continue

            m2 = ""

            if p2.match(line):
                m2 = p2.match(line)
            if p4.match(line):
                m2 = p4.match(line)

            if p6.match(line):
                m2 = p6.match(line)
            if p7.match(line):
                m2 = p7.match(line)
            if p8.match(line):
                m2 = p8.match(line)
            if p9.match(line):
                m2 = p9.match(line)
            if p10.match(line):
                m2 = p10.match(line)
            if p11.match(line):
                m2 = p11.match(line)
            if p12.match(line):
                m2 = p12.match(line)
            if p13.match(line):
                m2 = p13.match(line)
            if m2:
                group = m2.groupdict()
                for k, v in group.items():
                    if v:
                        if v.isdigit():
                            neighbor_dict.update({k:int(v)})
                        else:
                            neighbor_dict.update({k:v.lower()})
                continue
            m = p3.match(line)
            if m:
                group = m.groupdict()
                if group.pop('up') == 'up':
                    neighbor_dict.update({'up':True})
                else:
                    neighbor_dict.update({'up': False})

                for k, v in group.items():
                    if v:
                        if v.isdigit():
                            neighbor_dict.update({k:int(v)})
                        else:
                            neighbor_dict.update({k:v.lower()})
                continue

            m= p5.match(line)
            if m:
                neighbor_dict.update({'bfd':True})
                continue

            m = p14.match(line)
            if m:
                group = m.groupdict()
                mp_ref_gr = group.pop('cap_advertised')
                if 'mp' in mp_ref_gr:
                    neighbor_dict.update({'capmpadvertised':True})
                if 'refresh' in  mp_ref_gr:
                    neighbor_dict.update({'caprefreshadvertised': True})
                if 'gr' in  mp_ref_gr:
                    neighbor_dict.update({'capgrdynamicadvertised': True})

                mp_ref_gr_recvd = group.pop('cap_received')
                if 'mp' in mp_ref_gr_recvd:
                    neighbor_dict.update({'capmprecvd': True})
                if 'refresh' in mp_ref_gr_recvd:
                    neighbor_dict.update({'caprefreshrecvd': True})
                if 'gr' in mp_ref_gr_recvd:
                    neighbor_dict.update({'capgrdynamicrecvd': True})
                continue

            m = p15.match(line)
            if m:
                neighbor_dict.update({'capolddynamicadvertised': True})
                neighbor_dict.update({'capolddynamicrecvd':True})
                continue

            m = p16.match(line)
            if m:

                neighbor_dict.update({'caprradvertised': True})
                neighbor_dict.update({'caprrrecvd': True})
                continue

            m = p17.match(line)
            if m:
                group = m.groupdict()
                neighbor_dict.update({'capoldrradvertised': True})
                neighbor_dict.update({'capoldrrrecvd': True})
                continue

            m = p18.match(line)
            if m:
                group = m.groupdict()
                neighbor_dict.update({'capas4advertised': True})
                neighbor_dict.update({'capas4recvd': True})
                continue

            m = p19.match(line)
            if m:
                group = m.groupdict()
                af = group.pop('af_name').lower()
                af_dict = neighbor_dict.setdefault('af',{}).setdefault(af,{})
                if group.get('af_advertised') and group.get('af_advertised').strip() == 'advertised':
                    af_dict.update({'af_advertised':True})
                else:
                    af_dict.update({'af_advertised': False})
                if group.get('af_recvd') and  group.get('af_recvd').strip() == 'received':
                    af_dict.update({'af_recvd':True})
                else:
                    af_dict.update({'af_recvd': False})

                af_dict.update({'af_name':af})
                continue


            m = p20.match(line)
            if m:
                neighbor_dict.update({'capgradvertised':True})
                neighbor_dict.update({'capgrrecvd':True})
                continue

            m = p20_1.match(line)
            if m:
                gr_flag = True
                continue

            m = p21.match(line)
            if m:
                gr_adv_flag = True
                continue

            m = p22.match(line)
            if m:
                if gr_flag:
                    group = m.groupdict()
                    gr_dict = neighbor_dict.setdefault('graf', {})
                    gr_af_name_list = group.pop('gr_af_name').split("  ")
                    for gr_af in gr_af_name_list:
                        gr_af_name  = gr_af.lower()
                        graf_dict = gr_dict.setdefault(gr_af_name,{})
                        graf_dict.update({'gr_af_name':gr_af_name})
                        if gr_adv_flag:
                            graf_dict.update({'gr_adv': True})
                        if gr_recv_flag:
                            graf_dict.update({'gr_recv': True})
                        if gr_fwd_flag:
                            graf_dict.update({'gr_fwd': True})
                if recieve_flag:
                    group = m.groupdict()
                    capextendednh_af_name = group.pop('gr_af_name').lower()
                    cap_dict = neighbor_dict.setdefault('capextendednhaf',{}).setdefault(capextendednh_af_name,{})
                    cap_dict.update({'capextendednh_af_name': capextendednh_af_name})

                recieve_flag = gr_recv_flag = gr_adv_flag = gr_fwd_flag = False
                continue

            m = p23.match(line)
            if m:

                gr_recv_flag = True
                continue

            m = p24_1.match(line)
            if m:
                gr_fwd_flag = True
                continue

            m = p25.match(line)
            if m:
                group = m.groupdict()
                neighbor_dict.update({'grrestarttime': int(group.pop('grrestarttime'))})
                continue

            m = p26.match(line)
            if m:
                group = m.groupdict()
                neighbor_dict.update({'grstaletiem': int(group.pop('grstaletiem'))})
                continue

            m = p27.match(line)
            if m:
                group = m.groupdict()
                neighbor_dict.update({'grrecvdrestarttime': int(group.pop('grrecvdrestarttime'))})
                continue

            m = p28.match(line)
            if m:
                group = m.groupdict()
                capextendednhadvertised = group.pop('capextendednhadvertised')
                capextendednhrecvd = group.pop('capextendednhrecvd')
                if capextendednhadvertised == 'advertised':
                    neighbor_dict.update({'capextendednhadvertised': True})
                if capextendednhrecvd == 'received':
                    neighbor_dict.update({'capextendednhrecvd': True})
                continue

            m = p29.match(line)
            if m:
                gr_recv_flag = gr_adv_flag = gr_fwd_flag = False
                recieve_flag = True
                continue

            m3 = ""
            if p31.match(line):  m3 =  p31.match(line)
            if p32.match(line):  m3 =  p32.match(line)
            if p33.match(line):  m3 =  p33.match(line)
            if p34.match(line):  m3 =  p34.match(line)
            if p35.match(line) : m3 =  p35.match(line)
            if p36.match(line) : m3 =  p36.match(line)

            if p38.match(line) : m3 =  p38.match(line)


            if m3:
                group = m3.groupdict()
                neighbor_dict.update({k:int(v) for k,v in group.items()})
                continue

            m = p40.match(line)
            if m:
                group = m.groupdict()
                per_af_name = group.pop('per_af_name').lower()
                peraf_dict = neighbor_dict.setdefault('peraf',{}).setdefault(per_af_name,{})
                peraf_dict.update({'per_af_name': per_af_name})
                continue

            m = p41.match(line)
            if m:
                group = m.groupdict()
                peraf_dict.update({k:int(v) for k,v in group.items()})
                continue

            m = p42.match(line)
            if m:
                group = m.groupdict()
                peraf_dict.update({k: int(v) for k, v in group.items()})
                continue

            m = p43.match(line)
            if m:
                peraf_dict.update({'sendcommunity': True})
                continue

            m = p44.match(line)
            if m:
                peraf_dict.update({'sendextcommunity': True})
                continue


            m = p49.match(line)
            if m:
                group = m.groupdict()
                neighbor_dict.update({'localaddr': group.pop('localaddr')})
                neighbor_dict.update({'localport': int(group.pop('localport'))})
                continue
            m = p50.match(line)
            if m:
                group = m.groupdict()
                neighbor_dict.update({'remoteaddr':group.pop('remoteaddr')})
                neighbor_dict.update({'remoteport':int(group.pop('remoteport'))})
                continue

            m = p51.match(line)
            if m:
                group = m.groupdict()
                neighbor_dict.update({'fd':int(group.pop('fd'))})
                continue

            # Enhanced error processing: On                
            m = p52.match(line)
            if m:
                group = m.groupdict()['error_processing']

                if 'On' in group:
                    group = bool(group)

                processing_dict = neighbor_dict.setdefault\
                    ('enhanced_error_processing', {})
                
                processing_dict.update({'error_processing': group})
                continue
                    
            # 0 discarded attributes
            m = p53.match(line)
            if m:
                group = m.groupdict()
                processing_dict = neighbor_dict.setdefault\
                    ('enhanced_error_processing', {})

                processing_dict.update({'discarded_attr': \
                        int(group.pop('discarded_attr'))})

                continue

            # Last error length received: 0 
            m = p54.match(line)
            if m:
                neighbor_dict.update({'last_error_length_sent': \
                        int(m.groupdict().pop('last_error_length_sent'))})
                
                continue

            # Reset error value sent: 0
            m = p55.match(line)
            if m:
                neighbor_dict.update({'reset_error_value_sent': \
                        int(m.groupdict().pop('reset_error_value_sent'))})
                
                continue

            # Reset error sent major: 0 minor: 0
            m = p56.match(line)
            if m:
                neighbor_dict.update({'reset_error_sent_major': \
                    int(m.groupdict().pop('reset_error_sent_major'))})
                
                neighbor_dict.update({'reset_error_sent_minor': \
                    int(m.groupdict().pop('reset_error_sent_minor'))})
                
                continue

            # Last error length received: 0
            m = p57.match(line)
            if m:
                neighbor_dict.update({'last_error_length_received': \
                    int(m.groupdict().pop('last_error_length_received'))})
                continue

            # Reset error value received 0
            m = p58.match(line)
            if m:
                neighbor_dict.update({'reset_error_value_received': \
                    int(m.groupdict().pop('reset_error_value_received'))})
                
                continue

            # Reset error received major: 0 minor: 0
            m = p59.match(line)
            if m:
                neighbor_dict.update({'reset_error_received_major': \
                    int(m.groupdict().pop('reset_error_received_major'))})
                
                neighbor_dict.update({'reset_error_received_minor': \
                    int(m.groupdict().pop('reset_error_received_minor'))})

                continue

            # 10 accepted prefixes (10 paths), consuming 2360 bytes of memory
            m = p60.match(line)
            if m:
                neighbor_dict.update({'accepted_prefixes': \
                    int(m.groupdict().pop('accepted_prefixes'))})
                
                neighbor_dict.update({'memory_consumed_in_bytes': \
                    int(m.groupdict().pop('memory_consumed_in_bytes'))})
                
                continue

            # 0 received prefixes treated as withdrawn
            m = p61.match(line)
            if m:
                neighbor_dict.update({'received_prefixes': \
                    int(m.groupdict().pop('received_prefixes'))})
                
                continue

            # 40541 sent prefixes (40541 paths)
            m = p62.match(line)
            if m:
                neighbor_dict.update({'sent_prefixes': \
                    int(m.groupdict().pop('sent_prefixes'))})
                
                continue

            # Advertise GW IP is enabled
            m = p63.match(line)
            if m:
                if 'enabled' in m.groupdict('advertise_gw_ip'):
                    neighbor_dict.update({'advertise_gw_ip': \
                        bool(m.groupdict().pop('advertise_gw_ip'))})
                
                continue

            # Outbound route-map configured is GENIE_TEST, handle obtained
            m = p64.match(line)
            if m:
                neighbor_dict.update({'outbound_route_map': \
                    m.groupdict().pop('outbound_route_map')})
                
                continue

            # Last End-of-RIB received 00:00:11 after session start
            # Last End-of-RIB sent 00:00:06 after session start
            m = p65.match(line)
            if m:
                group = m.groupdict()
                if 'received' in group['action']:
                    neighbor_dict.update({'last_end_of_rib_received': \
                        group.pop('time')})
                
                if 'sent' in group['action']:
                    neighbor_dict.update({'last_end_of_rib_sent': \
                        group.pop('time')})
                
                continue

            # First convergence 00:00:06 after session start with 18810 routes sent
            m = p66.match(line)
            if m:
                neighbor_dict.update({'first_convergence': \
                    m.groupdict().pop('first_convergence')})
                neighbor_dict.update({'convergence_routes_sent': \
                    int(m.groupdict().pop('convergence_routes_sent'))})
                
                continue

        return result_dict

# ==========================================================================
#  schema for 'show bgp l2vpn evpn <WORD> | be "best path, in rib" n <WORD>'
# ==========================================================================
class ShowBgpL2vpnEvpnWordSchema(MetaParser):
    """Schema for show bgp l2vpn evpn <WORD> | be "best path, in rib" n <WORD>"""

    schema = {'mac_address':
                {Any():
                    {'next_hop': str,
                     'received_label': str}
                },
            }

# =============================================================
#  show bgp l2vpn evpn <WORD> | be "best path, in rib" n <WORD>
# =============================================================
class ShowBgpL2vpnEvpnWord(ShowBgpL2vpnEvpnWordSchema):
    """Parser for show bgp l2vpn evpn <WORD> | be "best path, in rib" n <WORD>"""
    """Parser for show bgp l2vpn evpn <WORD> | grep -b <WORD> -a <WORD> "best path"""

    cli_command = ['show bgp l2vpn evpn {mac} | grep -b {count1} -a {count2} "best path"','show bgp l2vpn evpn {mac} | be "best path, in rib" n {count2}']

    def cli(self, mac, count1, count2=None,output=None):
        if output is None:
            if mac and count1:
                if count2:
                    cmd = self.cli_command[0].format(mac=mac, count1=count1, count2=count2)
                else:
                    cmd = self.cli_command[1].format(mac=mac, count2=count1)
            else:
                cmd = ""
            out = self.device.execute(cmd)
        else:
            out = output

        ret_dict = {}

        p1 = re.compile(r'^(?P<next_hop>[0-9\.]+) +\(metric +(?P<metric>[0-9]+)\).*$')
        p2 = re.compile(r'^Received label +(?P<received_label>[0-9]+).*$')
        for line in out.splitlines():
            line = line.strip()

            # 10.9.0.101 (metric 9) from 10.4.0.66 (10.4.0.66)
            m = p1.match(line)
            if m:
                if 'mac_address' not in ret_dict:
                    ret_dict['mac_address'] = {}
                if mac not in ret_dict['mac_address']:
                    ret_dict['mac_address'][mac] = {}

                ret_dict['mac_address'][mac]['next_hop'] = \
                    str(m.groupdict()['next_hop'])
                continue

            # Received label 2001001
            m = p2.match(line)
            if m:

                if 'mac_address' not in ret_dict:
                    ret_dict['mac_address'] = {}
                if mac not in ret_dict['mac_address']:
                    ret_dict['mac_address'][mac] = {}

                ret_dict['mac_address'][mac]['received_label'] = \
                    str(m.groupdict()['received_label'])
                continue

        return ret_dict

# ==================================================================
#  schema for show bgp ipv4 mvpn route-type <route_type> vrf <vrf>
# ==================================================================
class ShowBgpIpMvpnRouteTypeSchema(MetaParser):
    """Schema for:
           show bgp ipv4 mvpn
           show bgp ipv4 mvpn route-type <route_type>
           show bgp ipv4 mvpn route-type <route_type> vrf <vrf>
           show bgp ipv4 mvpn route-type <route_type> vrf all"""

    schema = {
        'instance': {
            Any(): {
                'vrf': {
                    Any(): {
                        'vrf_name_out': str,
                        'address_family': {
                            Any(): {
                                'af_name': str,
                                'table_version': str,
                                'router_id': str,
                                'rd': {
                                    Any(): {
                                        Optional('rd_val'): str,
                                        Optional('rd_vrf'): str,
                                        'prefix': {
                                            Any(): {
                                                'nonipprefix': str,
                                                'path': {
                                                    Any(): {
                                                        'pathnr': int,
                                                        Optional('metric'): str,
                                                        Optional('statuscode'): str,
                                                        Optional('bestcode'): str,
                                                        Optional('typecode'): str,
                                                        'ipnexthop': str,
                                                        'weight': str,
                                                        Optional('path'): str,
                                                        'origin': str,
                                                        'localpref': str,
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }


# ===================================================================
#  Parser for show bgp ipv4 mvpn route-type <route_type> vrf <vrf>
# ===================================================================
class ShowBgpIpMvpnRouteType(ShowBgpIpMvpnRouteTypeSchema):
    """Parser for:
               show bgp ipv4 mvpn
               show bgp ipv4 mvpn route-type <route_type>
               show bgp ipv4 mvpn route-type <route_type> vrf <vrf>
               show bgp ipv4 mvpn route-type <route_type> vrf all"""

    cli_command = ['show bgp ipv4 mvpn route-type {route_type} vrf {vrf}','show bgp ipv4 mvpn route-type {route_type}',\
                   'show bgp ipv4 mvpn']
    exclude = [
      'path'
      'table_version']

    def cli(self, route_type="",vrf="",cmd="",output=None):
        if output is None:
            if not cmd:
                if vrf and route_type:
                    cmd = self.cli_command[0].format(route_type=route_type,vrf=vrf)
                if route_type and not vrf:
                    vrf = 'default'
                    cmd = self.cli_command[1].format(route_type=route_type)
                if not route_type and not vrf:
                    cmd = self.cli_command[2]
            out = self.device.execute(cmd)
        else:
            out = output
        result_dict = {}
        # BGP routing table information for VRF default, address family IPv4 MVPN
        p1 = re.compile(r'^\s*BGP +routing +table +information +for +VRF +(?P<vrf>\S+),'
                r' +address +family +(?P<af>[\w\s]+)$')

        # BGP table version is 390, Local Router ID is 10.16.2.2
        p2 = re.compile(r'^\s*BGP +table +version +is +(?P<table_version>[\d]+),'
                        r' +Local +Router +ID +is +(?P<router_id>[\d\.]+)$')

        #    Network            Next Hop            Metric     LocPrf     Weight Path
        # Route Distinguisher: 10.16.2.2:3    (L3VNI 10100)
        p3 = re.compile(r'^\s*Route +Distinguisher: +(?P<rd>[\d\.\:]+)'
                        r'( +\((L[2|3]VNI|Local VNI:) +(?P<rd_vrf>[\d]+)\))?$')

        # *>l[5][10.111.1.3][238.8.4.101]/64
        p4 = re.compile(r'^\s*(?P<statuscode>[s|S|x|d|h|>|s|*\s]+)?'
                            r'(?P<typecode>(i|e|c|l|a|r|I)+)?'
                            r'(?P<prefix>[\w\]\/\:\.\]\[]+)$')

        #                       Next Hop            Metric     LocPrf     Weight Path
        #                       10.196.7.7                           100          0 i
        # *>i                   10.196.7.7                           100          0 i
        #                       10.64.4.4                                        0 200 100 i
        #                       0.0.0.0                  0        100      32768 ?
        #                       10.64.4.4              219        0 10 3277 32768 36640 {27016} e
        p6 = re.compile(
            r'^\s*(?P<statuscode>[s|S|x|d|h|>|s|*\s]+)?(?P<typecode>('
            r'i|e|c|l|a|r|I)+)?\s+(?P<ipnexthop>[\d\.]+)?(?P<space1>\s+)?(?P<metric>['
            r'\d]+)?\s+(?P<localpref>[\d]+)\s+?(?P<weight>[\d]+)( +(?P<path>[0-9\{\}\s]+))? +(?P<origin>[i|e|c|l|a|I|?]+)$')

        for line in out.splitlines():
            if line:
                line = line.rstrip()
            else:
                continue

            m = p1.match(line)
            if m:
                group = m.groupdict()
                vrf = group['vrf']
                af = group['af'].lower()
                vrf_dict = result_dict.setdefault('instance', {}).\
                    setdefault('default', {}).setdefault('vrf', {}).\
                    setdefault(vrf, {})
                vrf_dict.update({'vrf_name_out': vrf})

                af_dict = vrf_dict.setdefault('address_family',{}).\
                    setdefault(af, {})
                af_dict.update({'af_name': af})
                continue

            m = p2.match(line)
            if m:
                group = m.groupdict()
                af_dict.update({'table_version': group['table_version']})
                af_dict.update({'router_id': group['router_id']})
                continue

            m = p3.match(line)
            if m:
                group = m.groupdict()
                rd = group['rd']
                rd_dict = af_dict.setdefault('rd', {}).setdefault(rd , {})
                rd_dict.update({'rd_val': rd})
                if group['rd_vrf']:
                    rd_dict.update({'rd_vrf': group['rd_vrf']})
                continue

            m = p4.match(line)
            if m:
                index = 0
                group = m.groupdict()
                bestcode= ""
                statuscode = ""
                prefix = group['prefix']
                prefix_dict = rd_dict.setdefault('prefix', {}).setdefault(prefix, {})
                prefix_dict.update({'nonipprefix': prefix})
                status_code = group.pop('statuscode')

                if status_code:
                    status_code = status_code.strip()
                    if len(status_code) > 1:
                        bestcode =  status_code[1]
                        statuscode = status_code[0]
                    else:
                        if '>' in status_code:
                            bestcode = status_code
                        else:
                            statuscode = status_code

                if group['typecode']:
                    typecode = group['typecode']
                continue

            m = p6.match(line)
            if m:
                index +=1
                group = m.groupdict()
                path_dict = prefix_dict.setdefault('path', {}).setdefault(index, {})
                path_dict.update({'pathnr': 0})
                type_code = group.pop('typecode')

                if type_code and index > 1:
                    path_dict.update({'typecode': type_code})
                elif typecode:
                    path_dict.update({'typecode':typecode})

                status_code = group.pop('statuscode')
                if not status_code:
                    if bestcode and index == 1:
                        path_dict.update({'bestcode':bestcode})
                    if statuscode and index == 1:
                        path_dict.update({'statuscode':statuscode})

                if status_code and index >1:
                    status_code = status_code.strip()
                    if len(status_code) > 1:
                        path_dict.update({'bestcode': status_code[1]})
                        path_dict.update({'statuscode': status_code[0]})
                    else:
                        if '>' in status_code:
                            path_dict.update({'bestcode': status_code})
                        else:
                            path_dict.update({'statuscode': status_code})
                if group['metric']:
                    path_dict.update({'metric': group['metric']})

                path_dict.update({'ipnexthop': group['ipnexthop']})
                path_dict.update({'weight': group['weight']})
                path_dict.update({'origin': group['origin']})
                path_dict.update({'localpref': group['localpref'] })
                if group['path']:
                    path_dict.update({'path': group['path']})
                continue

        if not len(list(Common.find_keys('rd', result_dict))) :
            result_dict = {}

        return result_dict

# ==========================================================
#  schema for show bgp ipv4 mvpn sa-ad detail vrf <vrf>
# ===========================================================
class ShowBgpIpMvpnSaadDetailSchema(MetaParser):
    """Schema for:
        show bgp ipv4 mvpn sa-ad detail vrf <vrf>"""

    schema = {
        'instance': {
            Any():{
                'vrf': {
                    Any(): {
                        'vrf_name_out': str,
                        'address_family': {
                            Any(): {
                                'af_name': str,
                                'rd': {
                                    Any(): {
                                        Optional('rd_val'): str,
                                        Optional('rd_vrf'): str,
                                        'prefix': {
                                            Any(): {
                                                'nonipprefix': str,
                                                'prefixversion': int,
                                                Optional('totalpaths'): int,
                                                'bestpathnr': int,
                                                Optional('mpath'): str,
                                                Optional('on_newlist'): bool,
                                                Optional('on_xmitlist'): bool,
                                                Optional('suppressed'): bool,
                                                Optional('needsresync'): bool,
                                                Optional('locked'): bool,
                                                'path': {
                                                    Any(): {
                                                        Optional('pathnr'): int,
                                                        'pathtype': str,
                                                        Optional('policyincomplete'): bool,
                                                        'pathvalid': bool,
                                                        'pathbest': bool,
                                                        Optional('pathdeleted'): bool,
                                                        Optional('pathstaled'): bool,
                                                        Optional('pathhistory'): bool,
                                                        Optional('pathovermaxaslimit'): bool,
                                                        Optional('pathmultipath'): bool,
                                                        Optional('pathnolabeledrnh'): bool,
                                                        'ipnexthop': str,
                                                        Optional('nexthop_status'):str,
                                                        'nexthopmetric': int,
                                                        'neighbor': str,
                                                        'neighborid': str,
                                                        Optional('origin'): str,
                                                        'localpref': int,
                                                        'weight': int,
                                                        Optional('inlabel'): int,
                                                        Optional('extcommunity'): list,
                                                        Optional('advertisedto'): list,
                                                        Optional('originatorid'): str,
                                                        Optional('clusterlist'): list,
                                                    }
                                                }
                                             }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }


# ===========================================================
#  Parser for show bgp ipv4 mvpn sa-ad detail vrf <vrf>
# ===========================================================
class ShowBgpIpMvpnSaadDetail(ShowBgpIpMvpnSaadDetailSchema):
    """parser for:
        show bgp ipv4 mvpn sa-ad detail
        show bgp ipv4 mvpn sa-ad detail vrf <vrf>
        show bgp ipv4 mvpn sa-ad detail vrf all"""
    cli_command = ['show bgp ipv4 mvpn sa-ad detail vrf {vrf}','show bgp ipv4 mvpn sa-ad detail']
    exclude = [
      'prefixversion', 
      'bestpathnr']

    def cli(self,vrf="",output=None):
        if output is None:
            if vrf:
                cmd = self.cli_command[0].format(vrf=vrf)
            else:
                cmd = self.cli_command[1]
            out = self.device.execute(cmd)
        else:
            out = output

        result_dict = {}

        # BGP routing table information for VRF default, address family IPv4 MVPN
        p1 = re.compile(r'^\s*BGP +routing +table +information +for +VRF +(?P<vrf_name_out>\S+),'
                        r' +address +family +(?P<af_name>[\w\s]+)$')

        # Route Distinguisher: 10.16.2.2:3    (L3VNI 10100)
        p2 = re.compile(r'^\s*Route Distinguisher: +(?P<rd>[\w\.\:]+)'
                        r'( +\((L[2|3]VNI|Local VNI:) +(?P<rd_vrf>[\d]+)\))?$')

        # BGP routing table entry for [5][10.111.1.3][238.8.4.s101]/64, version 388
        p3 = re.compile(
            r'^\s*BGP +routing +table +entry +for +(?P<nonipprefix>[\d\[\]\:\.\/]+),'
            r' +version +(?P<prefixversion>[\d]+)$')

        # Paths: (1 available, best #1)
        p4 = re.compile(r'^\s*Paths: +\((?P<totalpaths>[\d]+) +available,'
                        r' +best +#(?P<bestpathnr>[\d]+)\)$')

        # Flags: (0x000002)(high32 00000000) on xmit-list, is not in mvpn
        # Flags: (0x000002)(high32 00000000) on xmit-list, is not in mvpn, is not in HW
        p5 = re.compile(r'^\s*Flags: (?P<flag_xmit>[\S\s]+) +on +xmit-list'
            r'(, +(?P<flags_attr>[\w\s\/\,]+))?$')

        #   Advertised path-id 1
        p7 = re.compile(r'^\s*Advertised path-id +(?P<path_id>[\d]+)$')

        # Path type: local, path is valid, is best path, no labeled nexthop
        # Path type: internal, path is invalid(rnh not resolved),
        #        not best reason: Neighbor Address, no labeled nexthop
        p8 = re.compile(r'^\s*Path type: +(?P<path_type>[\w\s\(\)]+),'
                        r' +(?P<pathtypes>[\S\s\,\:\/\(\)]+)?$')

        #   AS-Path: NONE, path locally originated
        p9 = re.compile(
            r'^\s*AS-Path: +(?P<as_path>[\w]+)(, +path locally originated)?'
                r'(, +path sourced +(?P<internal_external>[\w]+) to AS)?$')

        #     0.0.0.0 (metric 0) from 0.0.0.0 (10.16.2.2)
        #     10.144.6.6 (inaccessible, metric 4294967295) from 10.64.4.4 (10.64.4.4)
        p10 = re.compile(
            r'^\s*(?P<ipnexthop>[\d\.]+) +\(((?P<nexthop_status>[\w]+), )?metric +(?P<nexthopmetric>[\d]+)\)'
            r' +from +(?P<neighbor>[\d\.]+)'
            r' +\((?P<neighborid>[\d\.]+)\)$')

        #       Origin IGP, MED not set, localpref 100, weight 32768
        p11 = re.compile(r'^\s*Origin +(?P<origin>[\w]+), +(MED +(?P<med>[\w\s]+),)?'
                         r' +localpref +(?P<localpref>[\d]+),'
                         r' +weight +(?P<weight>[\d]+)$')

        #       Extcommunity: RT:100:10100
        p12 = re.compile(r'^\s*Extcommunity: +(?P<extcommunity>[\w\s\:\.]+)$')

        # Originator: 10.144.6.6 Cluster list: 10.100.5.5 
        p13 = re.compile(r'^\s*Originator: +(?P<originatorid>[\d\.]+)'
                         r' +Cluster +list: +(?P<clusterlist>[\d\.]+)$')

        #   Path-id 1 advertised to peers:
        #     10.64.4.4            10.100.5.5        
        p14 = re.compile(r'^\s*Path-id +(?P<path_id>[\d]+) +advertised to peers:$')
        p15 = re.compile(r'^\s*(?P<advertisedto>[\d\s\.]+)$')


        for line in out.splitlines():
            if line:
                line = line.rstrip()
            else:
                continue

            m = p1.match(line)
            if m:
                group = m.groupdict()
                instance = 'default'
                vrf_name_out = group['vrf_name_out']
                af_name = group['af_name'].lower()
                continue

            m = p2.match(line)
            if m:
                group = m.groupdict()
                bgp_dict = result_dict.setdefault('instance', {}).setdefault(instance, {}).\
                                                setdefault('vrf', {}).setdefault(vrf_name_out, {})
                bgp_dict.update({'vrf_name_out': vrf_name_out})
                af_dict = bgp_dict.setdefault('address_family', {}).setdefault(af_name, {})
                af_dict.update({'af_name': af_name})
                rd = group['rd']
                rd_dict = af_dict.setdefault('rd',{}).setdefault(rd,{})
                rd_dict.update({'rd_val':rd})
                if group['rd_vrf']:
                    rd_dict.update({'rd_vrf': group['rd_vrf'].lower()})
                continue

            m = p3.match(line)
            if m:
                group = m.groupdict()
                nonipprefix = group['nonipprefix'].strip()
                prefix_dict = rd_dict.setdefault('prefix',{}).setdefault(nonipprefix,{})
                prefix_dict.update({'nonipprefix': nonipprefix})
                prefix_dict.update({'prefixversion': int(group['prefixversion'])})
                index = 0
                continue

            m = p4.match(line)
            if m:
                group = m.groupdict()
                prefix_dict.update({k:int(v) for k,v in group.items()})
                continue

            m = p5.match(line)
            if m:
                prefix_dict.update({'on_xmitlist':True})
                continue

            m = p7.match(line)
            if m:
                group = m.groupdict()
                path_temp_dict = prefix_dict.setdefault('path',{})
                continue

            m = p8.match(line)
            if m:
                index += 1
                path_temp_dict = prefix_dict.setdefault('path', {})
                path_dict = path_temp_dict.setdefault(index, {})
                path_dict.update({'pathnr': 0})
                group = m.groupdict()
                path_dict.update({'pathtype': group['path_type']})

                pathtypes = group.get('pathtypes')
                if 'path is valid' in pathtypes:
                    path_dict.update({'pathvalid': True})
                else:
                    path_dict.update({'pathvalid': False})

                if 'is best path' in pathtypes:
                    path_dict.update({'pathbest': True})
                else:
                    path_dict.update({'pathbest': False})

                if 'no labeled nexthop' in pathtypes:
                    path_dict.update({'pathnolabeledrnh': True})
                else:
                    path_dict.update({'pathnolabeledrnh': False})
                continue

            m = p10.match(line)
            if m:
                group = m.groupdict()
                path_dict.update({k:v for k,v in group.items()})
                path_dict.update({'nexthopmetric': int(group['nexthopmetric'])})
                if not group['nexthop_status']:
                    path_dict.pop('nexthop_status')
                continue

            m = p11.match(line)
            if m:
                group = m.groupdict()
                path_dict.update({'origin': group['origin'].lower()})
                path_dict.update({'localpref': int(group['localpref'])})
                path_dict.update({'weight': int(group['weight'])})
                continue

            m = p12.match(line)
            if m:
                group = m.groupdict()
                path_dict.update({k: sorted(v.split( )) for k, v in group.items()})
                continue

            m = p13.match(line)
            if m:
                group = m.groupdict()
                path_dict.update({'originatorid': group['originatorid']})
                path_dict.update({'clusterlist': sorted(group['clusterlist'].split( ))})
                continue


            m = p15.match(line)
            if m:
                group = m.groupdict()
                for k, v in group.items():
                    if k in path_dict:
                        path_dict[k].append(v)
                    else:
                        path_dict.update({k:v.split()})
                continue


        if 'instance' not in result_dict:
            return result_dict

        for instance in result_dict['instance']:
            if 'vrf' not in result_dict['instance'][instance]:
                continue
            for vrf in result_dict['instance'][instance]['vrf']:
                vrf_dict = result_dict['instance'][instance]['vrf'][vrf]
                if 'address_family' not in vrf_dict:
                    continue
                for af in vrf_dict['address_family']:
                    af_dict = vrf_dict['address_family'][af]
                    if 'rd' not in af_dict:
                        continue
                    for rd in af_dict['rd']:
                        if 'prefix' not in af_dict['rd'][rd]:
                            continue
                        for prefix in af_dict['rd'][rd]['prefix']:
                            if 'path' not in af_dict['rd'][rd]['prefix'][prefix]:
                                continue
                            for index in af_dict['rd'][rd]['prefix'][prefix]['path']:
                                if len(af_dict['rd'][rd]['prefix'][prefix]['path'][index].keys()) > 1:
                                    ind = 1
                                    next_dict = {}
                                    sorted_list = sorted(af_dict['rd'][rd]['prefix'][prefix]['path'].items(),
                                                         key=lambda x: x[1]['neighbor'])
                                    for i, j in enumerate(sorted_list):
                                        next_dict[ind] = af_dict['rd'][rd]['prefix'][prefix]['path'][j[0]]
                                        ind += 1
                                    del (af_dict['rd'][rd]['prefix'][prefix]['path'])
                                    af_dict['rd'][rd]['prefix'][prefix]['path'] = next_dict


        return result_dict

# ==================================================================
#  Parser for show bgp l2vpn evpn vrf <vrf>
# ==================================================================
class ShowBgpL2vpnEvpn(ShowBgpIpMvpnRouteType):
    """Parser for:
           show bgp l2vpn evpn
           show bgp l2vpn evpn vrf <vrf>
           show bgp l2vpn evpn vrf all"""

    cli_command = ['show bgp l2vpn evpn vrf {vrf}','show bgp l2vpn evpn']

    def cli(self, vrf="",output=None):
        if output is None:
            if vrf:
                cmd = self.cli_command[0].format(vrf=vrf)
            else:
                cmd = self.cli_command[1]
        else:
             cmd = ""
        return super().cli(cmd=cmd,output=output)


# ==================================================================
#  Parser for show bgp ipv4 mvpn
# ==================================================================
class ShowBgpIpMvpn(ShowBgpIpMvpnRouteType):
    """Parser for:
           show bgp ipv4 mvpn"""

    cli_command = 'show bgp ipv4 mvpn'

    def cli(self,output=None):
        if output is None:
            cmd = self.cli_command
        else:
            cmd = ""

        return super().cli(cmd=cmd,output=output)


