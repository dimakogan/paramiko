#!/usr/bin/env python

import hexdump
import sys

sys.path.insert(0,'..')

import paramiko
from paramiko import util
from paramiko.message import Message
from paramiko.transport import Transport

import pickle

try:
    import interactive
except ImportError:
    from . import interactive


# setup logging
paramiko.util.log_to_file('demo.log')

t = Transport("localhost:2222", resume=True)
kex_msg = Message(open("kexM.p", "rb").read())
K = pickle.load(open("K.p", "rb"))
H = pickle.load(open("H.p", "rb"))
session_id = pickle.load(open("SESSIONID.p", "rb"))
seqin = pickle.load(open("seqin.p", "rb"))
seqout = pickle.load(open("seqout.p", "rb"))

print "seqin: %u , seqout: %u" % (seqin, seqout)


t._parse_kex_init(kex_msg)
t._set_K_H(K, H)
t.session_id = session_id
t._activate_inbound()
t._activate_outbound()
t.packetizer._sequence_number_out = seqout
t.packetizer._sequence_number_in = seqin

print "Outbound Key:" + hexdump.dump(t.key_out) + ", IV:"  + hexdump.dump(t.IV_out)
#out = t.packetizer._Packetizer__block_engine_out.update("ABCDEFG")
#print "Encryption of 'ABCDEFG':" + hexdump.dump(out)


print "Begin Start Client"

t.start_client()
t.clear_to_send.set()

print "Opening Session"
chan = t.open_session()
print "Session Open"
chan.get_pty()
chan.invoke_shell()
interactive.interactive_shell(chan)
