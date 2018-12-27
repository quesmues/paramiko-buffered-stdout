# -*- coding: ISO-8859-1 -*-

import paramiko
import os
###################################################################################################
###################################################################################################
###################################################################################################

def conexao(host, user, senha):
    print("Conectando ao servidor "+host)
    cliente = paramiko.SSHClient()
    try:
        obj = open(os.path.join(os.path.dirname(__file__), 'know_hosts'), 'a')
        obj.close()
    except FileExistsError:
        print('Arquivo ja existe')
        pass
    cliente.load_host_keys(os.path.join(os.path.dirname(__file__), 'know_hosts'))
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cliente.connect(hostname=host, port=22, username=user, password=senha, timeout=10)
    return cliente


###################################################################################################
###################################################################################################
###################################################################################################

def line_buffered(std):
    line_buf = ""
    while not std.channel.exit_status_ready():
        line_buf += std.read(1).decode('utf-8')
        if line_buf.endswith('\n'):
            print(line_buf)
            yield line_buf
            line_buf = ''

def exeGrep(host, comando):
    try:
        user = 'cmpsn1'
        senha = 'Good4Now'
        cliente = conexao(host, user, senha)
    except:
        user = 'qalog'
        senha = 'V!V*2018@'
        cliente = conexao(host, user, senha)
    if cliente != 'error':
        stdoutlinhas = []
        stdin, stdout, stderr = cliente.exec_command(comando, bufsize=0)
        stdin.close()
        stderr.close()
        stdout.channel.settimeout(10)
        try:
            for l in line_buffered(stdout):
                stdoutlinhas.append(l)
        except Exception as e:
            print(e)
            pass
    cliente.close()
    return stdoutlinhas


###################################################################################################
###################################################################################################
###################################################################################################

def checarInstancia(host, servico):
    comando = 'sudo docker ps -a | grep '+servico
    retorno = exeGrep(host, comando)
    instancia = retorno[0]
    instancia = instancia.split(' ')
    instancia = instancia[0]
    return instancia

###################################################################################################
###################################################################################################
###################################################################################################

def coletarLog(pesquisa, host, instancia, linhas):
    if pesquisa:
        print(pesquisa, 'teste')
        comando = "sudo docker logs -f --since 10m "+instancia+" | grep -C "+linhas+" "+pesquisa
    else:
        comando = "sudo docker logs -f --since 10m " + instancia + " | grep -A " + linhas + " 1 "
        print(comando)
    retorno = exeGrep(host, comando)
    return retorno

###################################################################################################
###################################################################################################
###################################################################################################
instancia = ''
while instancia == '':
    instancia = checarInstancia('10.129.179.189', 'sigres-resource-allocation-xdsl')
pesquisa = ''
log = coletarLog(pesquisa, '10.129.179.189', instancia, '10000')
print(len(log))