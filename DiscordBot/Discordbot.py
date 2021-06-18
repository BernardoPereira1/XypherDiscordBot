from inspect import Arguments, Parameter
import os
import discord
from discord import message
from discord import embeds
from discord.embeds import Embed
from discord.ext import commands, tasks
import DiscordUtils
import asyncio
from datetime import datetime, timedelta
import csv
import pytz
from discord.utils import get



diretorio = '/home/ubuntu/Projetos-GitHub-Bernardo/DiscordBot/token.txt'
token = open(diretorio, "r").readline()


intents = discord.Intents().all()
client = discord.Client(command_prefix="!", intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")


# ID's e variaveis para uso geral
# Roles:
role_admin = 839182749452992640
role_aluno = 839182749452992639

# Salas de texto:
sala_texto_admin = 839182749758652557
sala_do_20 = 839182750673666124
sala_introducoes = 855157609577709579
sala_bemvindo = 839182749758652561


# ID's para o comando exame
# Roles:
aluno_id = '839182749452992639'


# Evento on_ready
@bot.event
async def on_ready():
    print('O bot está on')


@bot.event
async def on_message(message):
    """This function "on_ready" react to messages in a specific channel and deletes bad words.

    Args:
        None

    Returns:
        When someone sends a message on a specific channel the bot react to their message.
        The bot delete messages that contains bad words, this bad words are defined on a .txt file.
    """
    if (message.channel.id == sala_introducoes):
        await message.add_reaction('👋')

    diretorio = r'/home/ubuntu/Projetos-GitHub-Bernardo/DiscordBot/palavras.txt'
    with open(diretorio, "r", encoding='utf-8') as file:   
        file = file.read().split()

    for palavra in file:
        if palavra in message.content.lower():
            await message.delete()
            await message.channel.send(f'Não uses essa palavra aqui {message.author.mention}!')
    await bot.process_commands(message)


# Comando Olá
@bot.command(name='ola')
async def on_message(message):
    """This function makes the bot respond to the "ola" command.

    Args:
        None

    Returns:
        A message saying "Hello" together with the username of the person that gived the command.
    """
    await message.channel.send(f'Olá {message.author.mention} :grinning:')


# Comando para saber quantos membros existem no servidor
@bot.command(name='numeromembros')
async def on_message(ctx):
    """This function lets you know the number of people there are on the server by giving the command "numeromebros".

    Args:
        None

    Returns:
        The bot sends a message with the number of people.
    """
    await ctx.send('Há ' + str(ctx.guild.member_count) + ' membros no servidor')



@bot.command()
@commands.has_role(role_admin)
async def limpar(ctx, numero=2000):
    """This function let the admins erase 2000 messages or a specific amount of messages.

    Args:
        numero(int): The amount of messages.

    Returns:
        The bot purge the messages.
    """

    await ctx.channel.purge(limit=numero)


@bot.event
async def on_member_join(member):
    """This function welcome every one on the server.

    Args:
        None

    Returns:
        The bot welcome every one that enters in the server.
    """
    channel = bot.get_channel(sala_bemvindo)
    await channel.send(f"Bem vindo {member.mention} !")


# Comando Exame
@bot.command()
@commands.has_role(role_admin)
async def exame(ctx, inicioprova, primeirotempo, segundotempo, finalprova, link):
    """This function allows admins on the server to start an exam whenever they want.

    Args:
        inicioprova(int): Time in minutes till the exam starts.
        primeirotempo(int): The duration in minutes of the first time of the exam.
        segundotempo(int): The duration in minutes of the second time of the exam.
        finalprova(int): The duration in minutes of the last time of the exam.
        link(str): The link of the exam, for example a Google Drive link

    Note:
        The link needs to have the "https" part or it will not work.

    Returns:
        First the bot will send a "calendar" with the times when the things will happen.
        Then when it's time to start the exam the bot will send the exam link and a couple of instructions.
        When the times are up the bot sends a message with a link to fill a form and a couple of instructions, for example when the first
        time end the bot sends that link and tells you that you can stay until the second time end.
    """

    time = datetime.now(pytz.timezone('Europe/Lisbon'))

    # Variaveis utilizadas neste comando
    channel = bot.get_channel(sala_do_20)  # ID do canal "Sala do 20"
    provainicio = time + timedelta(minutes=int(inicioprova))
    periodo1 = provainicio + timedelta(minutes=int(primeirotempo))
    periodo2 = periodo1 + timedelta(minutes=int(segundotempo))
    tempofinal = periodo2 + timedelta(minutes=int(finalprova))

    # Informações sobre a prova
    await channel.send('-------------------------------------------------------------------------------------------------------------'
                       '\nInício da prova: ' + str(provainicio.strftime(r"%H:%M")) + 'H' + '\n1ºPeriodo até às: ' + str(periodo1.strftime(r"%H:%M")) + 'H' +
                       '\n2º período até às: ' + str(periodo2.strftime(r"%H:%M")) + 'H' + '\nFinal da prova às: ' + str(tempofinal.strftime(r"%H:%M")) + 'H \n'
                       '-------------------------------------------------------------------------------------------------------------')

    # Inicio da prova
    await asyncio.sleep(int(inicioprova) * 60)
    await channel.send('\nBem-vindos à Prova de Simulação de hoje \n<@&'+aluno_id+'> Juntem-se ao canal de voz: "Sala do 20" para começarmos\n')
    linkprova = discord.Embed()
    linkprova.description = f'Clica no link para teres acesso à prova: [link]({link})'
    await channel.send(embed=linkprova)
    await channel.send('-------------------------------------------------------------------------------------------------------------')

    # Fim do primeiro tempo
    await asyncio.sleep(int(primeirotempo) * 60)
    await channel.send('\n:alarm_clock:  Está concluído o primeiro período da prova :alarm_clock:\n')
    linkformulario = discord.Embed()
    linkformulario.description = "Se já terminaste preenche o formulário de check-out que está no link: [link](https://forms.gle/qDvEyYBUD2xGbvrN7)."
    await channel.send(embed=linkformulario)
    await channel.send('Se ainda não terminaste, podes continuar até ao segundo período\nNo final do dia publicaremos no fórum um post com os links para os critérios de correção e para o formulário de avaliação. Lembra-te de submeter o formulário de avaliação até quarta-feira ao final do dia.\n'
                       'Bom trabalho e bom fim-de-semana! <@&'+aluno_id+'> :point_up:\n'
                       '-------------------------------------------------------------------------------------------------------------')

    # Fim do segundo tempo
    await asyncio.sleep(int(segundotempo) * 60)
    await channel.send('\n:alarm_clock:  Está concluído o segundo período da prova :alarm_clock:\n')
    'Se ainda não terminaste, podes continuar até ao último período\n'
    linkformulario = discord.Embed()
    linkformulario.description = "Se já terminaste preenche o formulário de check-out que está no link: [link](https://forms.gle/qDvEyYBUD2xGbvrN7)."
    await channel.send(embed=linkformulario)
    await channel.send('Se ainda não terminaste, podes continuar até ao final da prova\nBom trabalho e bom fim-de-semana! <@&'+aluno_id+'> :point_up:\n'
                       '-------------------------------------------------------------------------------------------------------------')

    # Fim da prova
    await asyncio.sleep(int(finalprova) * 60)
    await channel.send('\n:alarm_clock: O tempo da prova acabou :alarm_clock:\n')
    linkformulario = discord.Embed()
    linkformulario.description = "Preenche o formulário de check-out que está no link: [link](https://forms.gle/qDvEyYBUD2xGbvrN7)."
    await channel.send(embed=linkformulario)
    await channel.send('Bom fim-de-semana! <@&'+aluno_id+'> :point_up:\n'
                       '-------------------------------------------------------------------------------------------------------------')



# Comando para saber quantas pessoas estão presentes no servidor e num canal especifico
@bot.command(name='presencas')
@commands.has_role(role_admin)
async def presencas(ctx, canal=None):
    """This function allows admins on the server to know how much people are online in a specific channel at the time that 
       the command "presencas" is given.

    Args:
        canal(str): The name of the channel.

    Note:
        If the name of the channel as spaces in it you need to use quotation marks or i will not work.

    Returns:
        The bot sends a csv file with the username and tag of the people present in the specified channel, 
        in addition it also shows the time at which these people were in the channel.
    """

    
    time = datetime.now(pytz.timezone('Europe/Lisbon'))

    if canal == None:

        pasta = '/home/ubuntu/Projetos-GitHub-Bernardo/DiscordBot/Presencas'
        ficheiro = 'presencas_' + str(datetime.now().date()) + '.csv'
        diretorio = os.path.join(pasta, ficheiro)

        await ctx.send('Presenças no servidor no dia: ' + str(datetime.now().date()) + ' às ' + time.strftime(r"%H:%M") + 'H')
        with open(diretorio, 'w', newline='', encoding='utf-8') as file:

            writer = csv.writer(file, delimiter=':', quoting=csv.QUOTE_NONE)
            writer.writerow(['Nome, tag, timestamp'])

            for user in ctx.guild.members:
                writer = csv.writer(file, delimiter='"',quoting=csv.QUOTE_NONE)

                if user.status != discord.Status.offline:
                    writer.writerow([user.name + ', ' + '#'+user.discriminator + ', ' + str(datetime.now().date()) + ' ' + time.strftime(r"%H:%M") + 'H'])

        await ctx.send(file=discord.File(diretorio))

    else:

        # Canal de onde a lista vem
        channel = get(ctx.guild.channels, name=str(canal))
        members = channel.members  # Encontra os membros que estão no canal

        pasta = '/home/ubuntu/Projetos-GitHub-Bernardo/DiscordBot/Presencas'
        ficheiro = 'presencas_canal_' + channel.name + '_' + str(datetime.now().date()) + '.csv'
        diretorio = os.path.join(pasta, ficheiro)

        await ctx.send('Presenças no canal ' + channel.name + ' no dia ' + str(datetime.now().date()) + ' às ' + time.strftime(r"%H:%M") + 'H')
        with open(diretorio, 'w', newline='', encoding='utf-8') as file:

            writer = csv.writer(file, delimiter=':', quoting=csv.QUOTE_NONE)
            writer.writerow(['Nome, tag, timestamp'])

            for user in members:
                writer = csv.writer(file, delimiter='"', quoting=csv.QUOTE_NONE)
                if user.status != discord.Status.offline:
                    writer.writerow([user.name + ', ' + '#'+user.discriminator + ', ' + str(datetime.now().date()) + ' ' + time.strftime(r"%H:%M") + 'H'])

        await ctx.send(file=discord.File(diretorio))


# Lembrete Eventos
@bot.command()
@commands.has_role(role_admin)
async def lembrete(ctx, arg):
    """This command creates a reminder that remind a certain role that they have events comming.

    Args:
        arg(str): This argument as two variations "sap" and "sp".

    Note:
        This command is not fully working.

    Returns:
        The bot sends a message warning the specified role that the event will start within a certain time. 
        This time is defined hardcoded in the variable "tempo_antecedencia".
    """

    if arg == 'sap':

        while True:

            time_sap = datetime.now(pytz.timezone('Europe/Lisbon')).time().replace(microsecond=0)
            formato_sap = '%H:%M:%S'
            tempo_antecedencia_sap = timedelta(hours=0, minutes=1, seconds=0)
            hora_sap = '00:38:00'
            lembrete_sap = (datetime.strptime(hora_sap, formato_sap) - tempo_antecedencia_sap).time()

            if time_sap == lembrete_sap:

                role_id_sap = 839182749452992639
                role_sap = get(ctx.guild.roles, id=int(role_id_sap))

                for user in role_sap.members:
                    message = 'Olá ' + user.name + '! ' + '\nNão te esqueças que a SAP começa dentro de ' + str(tempo_antecedencia_sap) + ' minutos! Vemo-nos no canal de voz "Auditório". Até já!'
                    await user.send(message)

                break

    if arg == 'sp':

        while True:

            time_sp = datetime.now(pytz.timezone('Europe/Lisbon')).time().replace(microsecond=0)
            formato_sp = '%H:%M:%S'
            tempo_antecedencia_sp = timedelta(hours=0, minutes=1, seconds=0)
            hora_sp = '00:40:00'
            lembrete_sp = (datetime.strptime(hora_sp, formato_sp) - tempo_antecedencia_sp).time()

            if time_sp == lembrete_sp:

                role_id_sp = 839182749452992639
                role_sp = get(ctx.guild.roles, id=int(role_id_sp))

                for user in role_sp.members:
                    message = 'Olá ' + user.name + '! ' + '\nNão te esqueças que o SP começa dentro de ' + str(tempo_antecedencia_sp) + ' minutos! Vemo-nos no canal de voz "Auditório". Até já!'
                    await user.send(message)

                break


# Grupo de comandos Ajuda, dá informações sobre os comandos
@bot.group(invoke_without_command=True)
async def ajuda(ctx):
    """This group of commands gives information about other commands.

    Args:
        exame(str): Use this to get info about "exame" command
        presencas(str): Use this to get info about "presencas" command
        lembrete(str): Use this to get info about "lembrete" command
        ola(str): Use this to get info about "ola" command
        numeromembros(str): Use this to get info about "numeromembros" command

    Note:
        If a normal user try to use this command to get info about admin commands it will not work.

    Returns:
        When the command "ajuda" is used the bot sends a list of the different commands that are on the server.
        If you want to get info about a command just use "ajuda" together with the name of the command.
    """

    embed = discord.Embed(title="Ajuda", description="Escreve !ajuda <comando> para obter informações sobre os mesmo!")

    embed.add_field(name="Comandos para admins", value="presencas,presencascanal, exame")
    embed.add_field(name="Comandos", value="ola, numeromembros")

    await ctx.send(embed=embed)


# Comando de ajuda(exame) só para admins
@ajuda.command()
@commands.has_role(role_admin)
async def exame(ctx):

    channel = bot.get_channel(sala_texto_admin)

    embed = discord.Embed(title="Comando Exame", description="Este comando permite começar um exame a qualquer hora")

    embed.add_field(name="Como utilizar?", value="Escreve !exame")
    embed.add_field(name="Onde se pode utilizar?", value="Em qualquer sala de texto")
    embed.add_field(name='Onde é que começa o exame?', value='Na sala de texto "Sala do 20"')

    await channel.send(embed=embed)


# Comando de ajuda(presencas) só para admins
@ajuda.command()
@commands.has_role(role_admin)
async def presencas(ctx):

    channel = bot.get_channel(sala_texto_admin)

    embed = discord.Embed(title="Comando Presenças", description="Este comando permite ver quantas pessoas estão online à hora que é dado o comando")
    embed.add_field(name="Como utilizar?", value="Escreve !presencas")
    embed.add_field(name="Onde se pode utilizar?", value="Em qualquer sala de texto")
    embed.add_field(name='Para onde são enviadas as presenças?', value='Para onde o comando foi dado')

    await channel.send(embed=embed)


# Comando de ajuda(olá)
@ajuda.command()
async def ola(ctx):

    embed = discord.Embed(title="Comando Olá", description='Este comando faz com que o bot te responda "Olá"')
    embed.add_field(name="Como utilizar?", value="Escreve !ola")
    embed.add_field(name="Onde se pode utilizar?", value="Em qualquer sala de texto")

    await ctx.send(embed=embed)


# Comando de ajuda(númeromembros)
@ajuda.command()
async def numeromembros(ctx):

    embed = discord.Embed(title="Comando Número de membros", description='Este comando permite ver o número de membros existentes no servidor')
    embed.add_field(name="Como utilizar?", value="Escreve !numeromembros")
    embed.add_field(name="Onde se pode utilizar?", value="Em qualquer sala de texto")

    await ctx.send(embed=embed)


# Comando FAQ
@bot.group(invoke_without_command=True)
async def faq(ctx):
    """This group of commands gives answers to frequently asked questions.

    Args:
        1(int): Use this if you want the answer to the first question on the list.
        2(int): Use this if you want the answer to the second question on the list.


    Returns:
        When the command "faq" is used the bot sends a list of the different questions that are frequently asked.
        If you want to get the answer about that question just use "faq" together with number of the question.
    """

    embed = discord.Embed(
        title="FAQ", description="Aqui estão algumas perguntas que são frequentemente feitas!")

    embed.add_field(name="Número 1", value="Como utilizar os comandos?", inline=False)
    embed.add_field(
        name="Número 2", value="Como envio as resoluções do plano semanal?", inline=False)

    await ctx.send(embed=embed)


# Comando de ajuda(exame) só para admins
@faq.command(aliases=['1'])
async def numero1(ctx):

    embed = discord.Embed(title="Como utilizar os comandos?", description=ctx.message.author.mention + ' usa "!" juntamente com o nome do comando')

    await ctx.send(embed=embed)


@faq.command(aliases=['2'])
async def numero2(ctx):

    embed = discord.Embed(title="Como envio as resoluções do plano semanal?", description=ctx.message.author.mention + ' tira uma fotografia e envia um email para resolucoes@overfit.study')

    await ctx.send(embed=embed)


# Loop que apaga mensagens de 24 em 24 horas
@tasks.loop(hours=24)
async def ApagaMensagens():
    """This function clears 3000 messages in the specified channels and after that the bot sends a message saying something
    and he will do this process every 24 hours.

    Args:
        None

    Returns:
        The bot sends a message after the channel is cleared.
    """

    auditorio = bot.get_channel(839182749758652565)
    sala1 = bot.get_channel(839182750166679622)
    sala2 = bot.get_channel(839182750166679623)
    sala3 = bot.get_channel(839182750166679624)
    sala4 = bot.get_channel(839182750166679625)
    sala5 = bot.get_channel(839182750166679626)
    sala6 = bot.get_channel(839182750166679627)

    for _ in range(30):
        await auditorio.purge()
        await sala1.purge()
        await sala2.purge()
        await sala3.purge()
        await sala4.purge()
        await sala5.purge()
        await sala6.purge()

    MessageAuditorio = await auditorio.send("Auditorio")
    await MessageAuditorio.pin()

    MessageSala1 = await sala1.send("Sala1")
    await MessageSala1.pin()

    MessageSala2 = await sala2.send("Sala2")
    await MessageSala2.pin()

    MessageSala3 = await sala3.send("Sala3")
    await MessageSala3.pin()

    MessageSala4 = await sala4.send("Sala4")
    await MessageSala4.pin()

    MessageSala5 = await sala5.send("Sala5")
    await MessageSala5.pin()

    MessageSala6 = await sala6.send("Sala6")
    await MessageSala6.pin()


@ApagaMensagens.before_loop
async def before():
    await bot.wait_until_ready()

ApagaMensagens.start()


bot.run(token.strip())
