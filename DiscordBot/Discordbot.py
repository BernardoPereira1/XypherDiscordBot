from inspect import Arguments, Parameter
from os import name
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


token = 'ODM5MTQ2NDIzMTMxNzAxMjc4.YJFaAQ.lD6YQsnYp9WYDR5ofDpgaENlp3U'


intents = discord.Intents().all()
client = discord.Client(command_prefix="!", intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")


# ID's e variaveis para uso geral
#Roles:
role_admin = 839182749452992640
role_aluno = 839182749452992639

#Salas de texto:
sala_texto_admin = 839182749758652557
sala_do_20 = 839182750673666124

#Variaveis
time = datetime.now(pytz.timezone('Europe/Lisbon'))


#ID's para o comando exame 
#Roles:
aluno_id = '839182749452992639'


# Evento on_ready
@bot.event
async def on_ready():
    print('O bot entrou')


# Comando Olá
@bot.command(name='ola')
async def on_message(message):
    await message.channel.send(f'Olá {message.author.mention} :grinning:')


# Comando Exame
@bot.command()
@commands.has_role(role_admin)
async def exame(ctx, inicioprova, primeirotempo, segundotempo, finalprova, link):

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


# Comando para saber quantos membros existem no servidor
@bot.command(name='numeromembros')
async def on_message(ctx):
    await ctx.send('Há ' + str(ctx.guild.member_count) + ' membros no servidor')


# Comando para saber quantas pessoas estão presentes no servidor e num canal especifico
@bot.command(name='presencas')
@commands.has_role(role_admin)
async def presencas(ctx, canal = None):
    if canal == None:
        
        await ctx.send('Presenças no servidor no dia: ' + str(datetime.now().date()) + ' às ' + time.strftime(r"%H:%M") + 'H')
        with open('presencas_' + str(datetime.now().date()) + '.csv', 'w', newline='') as file:

            writer = csv.writer(file, delimiter=':', quoting=csv.QUOTE_NONE)
            writer.writerow(['Nome, tag, timestamp'])

            for user in ctx.guild.members:
                writer = csv.writer(file, delimiter='"', quoting=csv.QUOTE_NONE)
                if user.status != discord.Status.offline:
                    writer.writerow([user.name + ', ' + '#'+user.discriminator + ', ' +str(datetime.now().date()) + ' ' + time.strftime(r"%H:%M") + 'H'])

        await ctx.send(file=discord.File(r'presencas_' + str(datetime.now().date()) + '.csv'))

    else:

        channel = bot.get_channel(int(canal))  # Canal de onde a lista vem
        members = channel.members  # Encontra os membros que estão no canal

        await ctx.send('Presenças no canal ' + channel.name + ' no dia ' + str(datetime.now().date()) + ' às ' + time.strftime(r"%H:%M") + 'H')
        with open('presencas_canal_' + channel.name + '_' + str(datetime.now().date()) + '.csv', 'w', newline='') as file:

            writer = csv.writer(file, delimiter=':', quoting=csv.QUOTE_NONE)
            writer.writerow(['Nome, tag, timestamp'])

            for user in members:
                writer = csv.writer(file, delimiter='"', quoting=csv.QUOTE_NONE)
                if user.status != discord.Status.offline:
                    writer.writerow([user.name + ', ' + '#'+user.discriminator + ', ' +str(datetime.now().date()) + ' ' + time.strftime(r"%H:%M") + 'H'])

        await ctx.send(file=discord.File(r'presencas_canal_' + channel.name + '_' + str(datetime.now().date()) + '.csv'))


# Lembrete Eventos
@bot.command()
async def lembrete(ctx, arg):
    
    if arg == 'sap':

        role = 839182749452992639
        minutos_antecedencia = 2
        hora_evento = datetime(time.year, time.month, time.day, 18, 15-int(minutos_antecedencia))
        lembrete = (hora_evento - time).total_seconds()
 
        await asyncio.sleep(lembrete)

        role = get(ctx.guild.roles, id=int(role))

        for user in ctx.guild.members:
            message = 'Olá ' + user.name + '! ' + '\nNão te esqueças que a SAP começa dentro de ' + str(minutos_antecedencia) + ' minutos! Vemo-nos no canal de voz "Auditório". Até já!'

            if role in user.roles:
                userDM = await user.create_dm() if (user.dm_channel is None) else user.dm_channel
                if userDM != None:
                    await userDM.send(message)
    
    if arg == 'sp':

        role = 839182749452992639
        minutos_antecedencia = 3
        hora_evento = datetime(time.year, time.month, time.day, 18, 15-int(minutos_antecedencia))
        lembrete = (hora_evento - time).total_seconds()
 
        await asyncio.sleep(lembrete)

        role = get(ctx.guild.roles, id=int(role))

        for user in ctx.guild.members:
            message = 'Olá ' + user.name + '! ' + '\nNão te esqueças que o SP começa dentro de ' + str(minutos_antecedencia) + ' minutos! Vemo-nos no canal de voz "Auditório". Até já!'
            if role in user.roles:
                userDM = await user.create_dm() if (user.dm_channel is None) else user.dm_channel
                if userDM != None:
                    await userDM.send(message)



# Grupo de comandos Ajuda, dá informações sobre os comandos
@bot.group(invoke_without_command=True)
async def ajuda(ctx):

    embed = discord.Embed(
        title="Ajuda", description="Escreve !ajuda <comando> para obter informações sobre os mesmo!")

    embed.add_field(name="Comandos para admins",
                    value="presencas,presencascanal, exame")
    embed.add_field(name="Comandos", value="ola, numeromembros")

    await ctx.send(embed=embed)


# Comando de ajuda(exame) só para admins
@ajuda.command()
@commands.has_role(role_admin)
async def exame(ctx):

    channel = bot.get_channel(sala_texto_admin)

    embed = discord.Embed(
        title="Comando Exame", description="Este comando permite começar um exame a qualquer hora")
    embed.add_field(name="Como utilizar?", value="Escreve !exame")
    embed.add_field(name="Onde se pode utilizar?",
                    value="Em qualquer sala de texto")
    embed.add_field(name='Onde é que começa o exame?',
                    value='Na sala de texto "Sala do 20"')

    await channel.send(embed=embed)



# Comando de ajuda(presencas) só para admins
@ajuda.command()
@commands.has_role(role_admin)
async def presencas(ctx):

    channel = bot.get_channel(sala_texto_admin)

    embed = discord.Embed(title="Comando Presenças",
                          description="Este comando permite ver quantas pessoas estão online à hora que é dado o comando")
    embed.add_field(name="Como utilizar?", value="Escreve !presencas")
    embed.add_field(name="Onde se pode utilizar?",
                    value="Em qualquer sala de texto")
    embed.add_field(name='Para onde são enviadas as presenças?',
                    value='Para onde o comando foi dado')

    await channel.send(embed=embed)


# Comando de ajuda(presencascanal) só para admins
@ajuda.command()
@commands.has_role(role_admin)
async def presencascanal(ctx):

    channel = bot.get_channel(sala_texto_admin)

    embed = discord.Embed(title="Comando Presenças Canal",
                          description="Este comando permite ver quantas pessoas estão online numa sala à hora que é dado o comando")
    embed.add_field(name="Como utilizar?",
                    value="Escreve o comando !presencascanal juntamente com o id do canal desejado")
    embed.add_field(name="Onde se pode utilizar?",
                    value="Em qualquer sala de texto")
    embed.add_field(name='Para onde são enviadas as presenças?',
                    value='Para onde o comando foi dado')

    await channel.send(embed=embed)


# Comando de ajuda(olá)
@ajuda.command()
async def ola(ctx):

    embed = discord.Embed(
        title="Comando Olá", description='Este comando faz com que o bot te responda "Olá"')
    embed.add_field(name="Como utilizar?", value="Escreve !ola")
    embed.add_field(name="Onde se pode utilizar?",
                    value="Em qualquer sala de texto")

    await ctx.send(embed=embed)


# Comando de ajuda(númeromembros)
@ajuda.command()
async def numeromembros(ctx):

    embed = discord.Embed(title="Comando Número de membros",
                          description='Este comando permite ver o número de membros existentes no servidor')
    embed.add_field(name="Como utilizar?", value="Escreve !numeromembros")
    embed.add_field(name="Onde se pode utilizar?",
                    value="Em qualquer sala de texto")

    await ctx.send(embed=embed)


# Loop que apaga mensagens de 24 em 24 horas
@tasks.loop(hours=24)
async def ApagaMensagens(amount=5000000000):
    sala1 = bot.get_channel(839182750166679622)

    messagessala1 = []

    async for message in sala1.history(limit=amount + 1):
        messagessala1.append(message)

    await sala1.delete_messages(messagessala1)


@ApagaMensagens.before_loop
async def before():
    await bot.wait_until_ready()
    print("Pronto para apagar")


ApagaMensagens.start()


bot.run(token)

