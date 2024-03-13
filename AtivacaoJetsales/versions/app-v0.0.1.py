from flask import Flask, render_template, request, redirect, url_for, session
import os
import yaml
import subprocess
import logging

app = Flask(__name__)

app.secret_key = os.urandom(24)

diretorio_logs = os.path.join(os.path.dirname(__file__), '../logs')

if not os.path.exists(diretorio_logs):
    os.makedirs(diretorio_logs)

logging.basicConfig(filename=os.path.join(diretorio_logs, 'app.log'), level=logging.INFO)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sistema = request.form['sistema']
        project_name = request.form['project_name'].strip()
        ip_address = request.form['ip_address']
        playbook_projeto = f'ativacao-{sistema.replace(" ","")}-jet.yml'

        session['project_name'] = project_name
        session['playbook_projeto'] = playbook_projeto

        logging.info(f"Definindo projeto: {project_name}, playbook: {playbook_projeto}")

        # Criando o dicionário para o inventário Ansible
        inventory = {
            'all': {
                'hosts': {
                    project_name: {
                        'ansible_ssh_host': ip_address,
                        'projeto': project_name,
                        'playbook_projeto': playbook_projeto,
                        'ansible_user': 'deploy',
                        'ansible_password': 'JqasPCCz6iwaTDk',
                        'sudo_pass': 'qLeGgkBn6hfBY0RLg16NiB0c6j2ip',
                        'zabbix_hostname': "{{inventory_hostname}}",
                        'hostname': "{{ zabbix_hostname }}",
                        'domain': f"{project_name}.jetsalesbrasil.com",
                        'domain_api': f"{project_name}api.jetsalesbrasil.com",
                        'swap_file': "/swapfile",
                        'swap_space': "{{ (ansible_memtotal_mb * 0.3) | int }}M",
                        'root_pass': 'C4str0491!!',
                        'srv_telegraf': 'grafana.jetsalesbrasil.com',
                    }
                }
            }
        }

        diretorio_inventario = os.path.abspath(os.path.join(os.path.dirname(__file__), "../inventarios/"))

        if not os.path.exists(diretorio_inventario):
            os.makedirs(diretorio_inventario)

        nome_arquivo = f"{project_name}.yml"
        caminho_arquivo = os.path.join(diretorio_inventario, nome_arquivo)

        with open(caminho_arquivo, 'w') as outfile:
            yaml.dump(inventory, outfile, default_flow_style=False)

        # Mensagem a ser exibida na próxima página
        message = f"Inventário gerado com sucesso em ../AtivacaoJetsales/inventarios/{project_name}.yml. O playbook a ser executado é o {playbook_projeto}."
        logging.info(message)

        return render_template('success.html', message=message, inventory=inventory['all']['hosts'], project_name=project_name)

    return render_template('index.html')

@app.route('/run_ansible', methods=['GET'])
def run_ansible():
    # Recuperando os dados da sessão
    project_name = session.get('project_name', 'default_project')
    playbook_projeto = session.get('playbook_projeto', 'default_playbook')

    # Montando o comando para executar o Ansible
    playbook_command = f"ansible-playbook -i ../AtivacaoJetsales/inventarios/{project_name}.yml ../AtivacaoJetsales/{playbook_projeto}"
    logging.info(f"Executando o comando: {playbook_command}")

    # Tentando executar o comando
    try:
        output = subprocess.check_output(playbook_command, shell=True, stderr=subprocess.STDOUT, text=True)
        logging.info(f"Saída do comando: {output}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro durante a execução do comando. Saída: {e.output}")

    return redirect('index.html')

if __name__ == '__main__':
    app.run(host='127.12.9.12', port=5000,debug=True)
