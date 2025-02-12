import socket, requests, json, select, re

class QQ_API:
        def __init__(self):
                with open("./config.json", 'r', encoding = 'utf-8') as f:
                        self.config = json.loads(f.read())
        def Data_Analysis(self, link_socket, request):
                # 查找json
                for i in range(len(request)):
                        if request[i] == '{':
                                request = request[i:]
                                break
                for i in range(len(request)):
                        if request[len(request) - i - 1] == '}':
                                request = request[:len(request) - i]
                                break
                print(request)
                body = json.loads(request)
                # 处理消息
                if body['message_type'] == "group":
                        print('[MSG] 接收[group(' + str(body['group_id']) + ')' + str(body['sender']['nickname']) + '(' + str(body['user_id']) + ')]: ' + str(body['raw_message']))
                elif body['message_type'] == "private":
                        print('[MSG] 接收[' + str(body['sender']['nickname']) + '(' + str(body['user_id']) + ')]: ' + str(body['raw_message']))
                for i in range(len(body['message'])):
                        if body['message'][i]['type'] == "at" and body['message'][i]['data']['qq'] == self.config['bot number']:
                                print('[MSG] 接收[at]')
                        if body['message'][i]['type'] == "text":
                                raw_message = body['message'][i]['data']['text']
                                print('[MSG] 接收[text]')
                
                resposne_header = "HTTP/1.1 200 OK\r\n"
                resposne_header += "\r\n"
                link_socket.send(resposne_header.encode("utf-8"))


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
