import socket, requests, json, select
from yunAi_api import YunAi_API
from napcat_api import Napcat_API
from loguru import logger

class QQ_API:
        def __init__(self):
                with open("./config.json", 'r', encoding = 'utf-8') as f:
                        self.config = json.loads(f.read())
                self.yunAi_API = YunAi_API(self.config['yun key'], self.config['yun url'], self.config['yun model'])
                self.napcat_API = Napcat_API(self.config['napcat url'], self.config['napcat post port'], self.config['post token'])
        def Data_Analysis(self, link_socket, request):
                send_flag = False
                # 查找json
                for i in range(len(request)):
                        if request[i] == '{':
                                request = request[i:]
                                break
                for i in range(len(request)):
                        if request[len(request) - i - 1] == '}':
                                request = request[:len(request) - i]
                                break
                logger.debug(request)
                body = json.loads(request)
                # 处理消息
                for i in range(len(body['message'])):
                        if body['message'][i]['type'] == "at" and body['message'][i]['data']['qq'] == self.config['bot number']:
                                send_flag = True
                        if body['message'][i]['type'] == "text":
                                sendToChat_message = body['message'][i]['data']['text']
                # 回复
                if body['message_type'] == "group":
                        # print('[MSG] 接收[group(' + str(body['group_id']) + ')' + str(body['sender']['nickname']) + '(' + str(body['user_id']) + ')]: ' + str(body['raw_message']))
                        if send_flag == True and sendToChat_message:
                                logger.info('接收群at, [group('+ str(body['group_id']) + ')' + str(body['sender']['nickname']) + '(' + str(body['user_id']) + ')]: ' + sendToChat_message)
                                back_message = self.yunAi_API.Chat_Send(sendToChat_message)
                                logger.info('回复群at: ' + back_message)
                                self.napcat_API.send_group_msg(body['group_id'], body['message_id'], back_message)
                elif body['message_type'] == "private":
                        # print('[MSG] 接收[' + str(body['sender']['nickname']) + '(' + str(body['user_id']) + ')]: ' + str(body['raw_message']))
                        if sendToChat_message:
                                logger.info('接收私聊，['+ str(body['sender']['nickname']) + '(' + str(body['user_id']) + ')]: ' + sendToChat_message)
                                back_message = self.yunAi_API.Chat_Send(sendToChat_message)
                                logger.info('回复私聊: ' + back_message)
                                self.napcat_API.send_private_msg(body['user_id'], back_message)


                # resposne_header = "HTTP/1.1 200 OK\r\n"
                # resposne_header += "\r\n"
                # link_socket.send(resposne_header.encode("utf-8"))

                


        def QQ_Loop(self):
                qq_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                qq_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                qq_server.bind(('0.0.0.0', self.config['napcat event port']))
                qq_server.listen(128)
                qq_server.setblocking(False)
                epl = select.epoll()
                epl.register(qq_server.fileno(), select.EPOLLIN)
                fd_event_dict: dict = {}
                while True:
                        try:
                                fd_event_list: list = epl.poll()
                                for fd, event in fd_event_list:
                                        if fd == qq_server.fileno():
                                                client, info = qq_server.accept()
                                                epl.register(client.fileno(), select.EPOLLIN)
                                                fd_event_dict[client.fileno()] = client
                                        elif event == select.EPOLLIN:
                                                recv_data: str = fd_event_dict[fd].recv(4096).decode("utf-8")
                                                if recv_data:
                                                        self.Data_Analysis(fd_event_dict[fd], recv_data)
                                                else:
                                                        fd_event_dict[fd].close()
                                                        epl.unregister(fd)
                                                        del fd_event_dict[fd]
                        except Exception as e:
                                logger.error(f"{e}")
