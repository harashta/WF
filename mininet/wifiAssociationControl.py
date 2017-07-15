from mininet.wifiLink import link
from mininet.log import debug

class associationControl (object):

    changeAP = False

    def __init__(self, sta, ap, wlan, ac):
        self.customAssociationControl(sta, ap, wlan, ac)

    def customAssociationControl(self, sta, ap, wlan, ac):
        """Mechanisms that optimize the use of the APs
        llf: Least-loaded-first
        ssf: Strongest-signal-first"""
        if ac == "llf":
            apref = sta.params['associatedTo'][wlan]
            if apref != '':
                ref_llf = len(apref.params['associatedStations'])
                if len(ap.params['associatedStations']) + 2 < ref_llf:
                    debug('iw dev %s disconnect' % sta.params['wlan'][wlan])
                    sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
                    self.changeAP = True
            else:
                self.changeAP = True
        elif ac == "ssf":
            distance = link.getDistance(sta, sta.params['associatedTo'][wlan])
            RSSI = link.setRSSI(sta, sta.params['associatedTo'][wlan], wlan, distance)
            refDistance = link.getDistance(sta, ap)
            refRSSI = link.setRSSI(sta, ap, wlan, refDistance)
            if float(refRSSI) > float(RSSI + 0.1):
                debug('iw dev %s disconnect' % sta.params['wlan'][wlan])
                sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
                self.changeAP = True
        elif ac == "coba":
            apref = sta.params['associatedTo'][wlan]
            distance = link.getDistance(sta, sta.params['associatedTo'][wlan])
            RSSI = link.setRSSI(sta, sta.params['associatedTo'][wlan], wlan, distance)
            refDistance = link.getDistance(sta, ap)
            refRSSI = link.setRSSI(sta, ap, wlan, refDistance)
            if apref != '':
                ref_llf = len(apref.params['associatedStations'])
#                for p in apref.params:
#                    debug(apref.params['associatedStations'][wlan])
                if len(ap.params['associatedStations']) + 2 < ref_llf:
                    if float(refRSSI) > float(RSSI + 0.1):
                    #if float(RSSI) < float(-41.00):
                        debug(' %s disconnect  1\n' % sta.params['wlan'][wlan])
                        sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
                        self.changeAP = True
                    else:
                        debug(' %s gausah pindah 1 \n' % sta.params['wlan'][wlan])
                """elif len(ap.params['associatedStations']) + 2 > ref_llf:
                    if float(refRSSI) > float(RSSI + 0.1):
                        debug(' %s disconnect  2\n' % sta.params['wlan'][wlan])
                        sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
                        self.changeAP = True
                    elif float(refRSSI) < float(RSSI + 0.1):
                        debug(' %s disconnect 3\n' % sta.params['wlan'][wlan])
                        sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
                        self.changeAP = True
                    else:
                        debug(' %s gausah pindah 2 \n' % sta.params['wlan'][wlan])
                else:
                    debug('= bukan 2-2nya\n')"""
            else:
                self.changeAP = True
                debug('apref kopong\n')

        return self.changeAP
