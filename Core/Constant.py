# -*- coding: UTF-8 -*-

# 消息头 消息体的大小 4字节 最大1G的打包
# 消息类型 2字节
# 消息体 任意字节
MessageHead = 4
MessageType = 8

def get_size_msg_head():
	return MessageHead + MessageType
