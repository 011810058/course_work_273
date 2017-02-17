"""
Module: socket-mon.py
Descritpion: To implement functions using psutil
Created By: Jasmeet Singh (011810058)
"""
from operator import itemgetter
from itertools import groupby
import psutil

class SocketMonitor(object):
    """ This class provide function to get and print list of sockets with status"""

    def __init__(self):
        self.socket_list = []

    def get_socket_detail(self):
        """get_socket_detail: Return list of socket connections"""

        try:
            for socket_conn in psutil.net_connections(kind='inet'):
                if socket_conn.laddr != () and socket_conn.raddr != ():
                    self.socket_list.append([socket_conn.pid, socket_conn.laddr, \
                    socket_conn.raddr, socket_conn.status])
            return self.socket_list
        except Exception as ex:
            print ex.message
            raise

    def ordered_socket_list(self, socket_list):
        """
        ordered_socket_list: To print socket in order of no of occurence
        Input: socket_list
        """

        socket_ordered_list = []
        for process_id, process_group in groupby(socket_list, key=itemgetter(0)):
            socket_ordered_list.append([process_id, len(list(process_group))])
        socket_ordered_list.sort(key=itemgetter(1), reverse=True)

        print "\"%8s\", \"%s\" , \"%s\", \"%s\"" % ("pid", "laddr", "raddr", "status")
        for process_id in socket_ordered_list:
            for socket_record in socket_list:
                if socket_record[0] == process_id[0]:
                    laddr, lport = socket_record[1]
                    raddr, rport = socket_record[2]
                    print "\"%8s\", \"%s@%s\", \"%s@%s\", \"%s\"" % \
                    (socket_record[0], laddr, lport, raddr, rport, socket_record[3])
                    #print ','.join(map(str, socket_record))

def main():
    """ To print output of the sockets"""
    socket_monitor = SocketMonitor()
    socket_detail = socket_monitor.get_socket_detail()
    socket_monitor.ordered_socket_list(socket_detail)

if __name__ == "__main__":
    main()
