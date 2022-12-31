import discord
from discord import Guild, app_commands
from discord.utils import get
from datetime import datetime
from datetime import date, timedelta
from discord.ui import Button, View
from discord import ui
import youtube_dl
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f'{self.user}이 시작되었습니다')  #  봇이 시작하였을때 터미널에 뜨는 말
        game = discord.Game('테스트')          # ~~ 하는중
        await self.change_presence(status=discord.Status.idle, activity=game)

client = aclient()
tree = app_commands.CommandTree(client)

class my_modal(ui.Modal, title = "민원 제기"):
    answer = ui.TextInput(label = "민원", style = discord.TextStyle.long, placeholder = "왜 거부처리가 부당하다고 생각하는지 자세히 적어주세요", default = "-", required = True, max_length = 500)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(title = "민원 제기 완료", description=f"민원이 제기 제기되었습니다.", color=0x4000FF)
        embed.add_field(name="사유", value="`{}`".format(self.answer),inline=False)
        await interaction.followup.send(embed=embed)
        ch = client.get_channel(1048566346755100702)
        embed1 = discord.Embed(title = "입국 거부 민원 접수", description=f"**민원 제기 사유**\n{self.answer}", timestamp = datetime.now(), color=0x4000FF)
        await ch.send(embed=embed1)


class j_modal(ui.Modal, title = "입국 요청"):
    answer = ui.TextInput(label = "가입 경로가 어떻게 되시나요?", style = discord.TextStyle.short, placeholder = "ex) 지인 추천", default = "-", required = True, max_length = 100)
    answer2 = ui.TextInput(label = "로블록스 닉네임이 어떻게 되시나요?", style = discord.TextStyle.short, placeholder = "디플닉 x", default = "-", required = True, max_length = 50)

    async def on_submit(self, interaction: discord.Interaction):
        ablerole = get(interaction.user.guild.roles, id=1037736870190256181)
        able = ablerole in interaction.user.roles
        if able == True:
            embed = discord.Embed(title="감사합니다", description="ㅤ", color=0x4000FF)  # 문의 보낸 후 결과 임베드
            embed.add_field(name="가입 메시지가 전달되었습니다.", value="ㅤ", inline=False)
            embed.add_field(name="가입 경로", value="`{}`\n".format(self.answer), inline=False)  # 문의 내용
            embed.add_field(name="로블록스 닉네임", value="`{}`\n".format(self.answer2), inline=False)  # 문의 내용
            embed.add_field(name="ㅤ", value="**▣ 입국 요청에 대한 답장은 가입지원팀원이 확인후\n답장이 오니 기다려 주시면 감사하겠습니다**", inline=False)
            embed.add_field(name="ㅤ", value="- **명예특별시 가입지원팀 일동** -", inline=False)  # 관리자 이름
            nick = '가입 대기중ㅣ{}'.format(self.answer2)
            await interaction.user.edit(nick=nick)
            await interaction.response.send_message(embed=embed, ephemeral = True)

            role = get(interaction.guild.roles, id=1058617602517237901)
            embed1 = discord.Embed(title="명령어 사용 감지됨", description="{} 가 <#{}> 에서 /입국요청 명령어를 사용했습니다.".format(interaction.user.mention, interaction.channel_id), color=0x4000FF)   # 답변 임베드
            ch = client.get_channel(1048251272010158130)
            await ch.send(embed=embed1)
            embed = discord.Embed(title="가입자 알림", description="ㅤ", color=0x4000FF)  # 문의 보낸 후 결과 임베드
            embed.add_field(name="가입자 디스코드 계정", value="{}".format(interaction.user.mention), inline=False)  # 문의 내용
            embed.add_field(name="가입자 로블록스 계정", value="{}".format(self.answer2), inline=False)
            embed.add_field(name="가입자 가입경로", value="{}".format(self.answer), inline=False)
            log = client.get_channel(1048246871207981117)
            await log.send(embed=embed) # 그 사람에게 올 유저 ID와 문의 내용
            await interaction.user.add_roles(role)
        if able == False:
            embed = discord.Embed(title="ERROR", description="이미 입국된 상태입니다.", color=0x4000FF)  # 문의 보낸 후 결과 임베드
            await interaction.response.send_message(embed=embed, ephemeral = True)

@tree.command(name = '입국요청', description = '명예특별시 시민이 되어보세요')  # 문의 명령어
async def slash2(interaction: discord.Interaction):  # 옵션
    await interaction.response.send_modal(j_modal())


@tree.command(name = '입국승낙', description = '가입 대기자의 입국을 승낙합니다')  # 문의 명령어
async def slash2(interaction: discord.Interaction, 유저:discord.Member):  # 옵션

    ablerole = get(interaction.user.guild.roles, id=1058613051152150578)
    waitrole = get(interaction.user.guild.roles, id=1058617602517237901)
    able = ablerole in interaction.user.roles
    waitbool = waitrole in 유저.roles

    if able == True:
        if waitbool == True:
            embed = discord.Embed(title="승낙 완료", description="ㅤ", color=0x4000FF)  # 문의 보낸 후 결과 임베드
            embed.add_field(name="가입 대기자의 입국을 승낙했습니다.", value="ㅤ", inline=False)
            role = get(interaction.user.guild.roles, id=1037736471739768903)
            rrole = get(interaction.user.guild.roles, id=1037736870190256181)
            rrole2 = get(interaction.user.guild.roles, id=1058617602517237901)
            await 유저.add_roles(role)
            await 유저.remove_roles(rrole)
            await 유저.remove_roles(rrole2)
            await interaction.response.send_message(embed=embed, ephemeral = True)

            embed1 = discord.Embed(title="명령어 사용 감지됨", description="{} 가 <#{}> 에서 /입국승낙 명령어를 사용했습니다.".format(interaction.user.mention, interaction.channel_id), color=0x4000FF)   # 답변 임베드
            ch = client.get_channel(1048251272010158130)
            await ch.send(embed=embed1)
            embed2 = discord.Embed(title="입국이 승낙되었습니다!", description="명예특별시민 역할이 지급되었으며 이제 명예특별시 디스코드에서 활동할 수 있습니다.", color=0x4000FF)  # 문의 보낸 후 결과 임베드
            await 유저.send(embed=embed2)
            nonick = 유저.nick
            nick1 = '명예특별시민ㅣ{}'.format(nonick[7:])
            await 유저.edit(nick=nick1)
        if waitbool == False:
            embed = discord.Embed(title="ERROR", description="승낙 대상이 입국 요청을 하지 않았거나 입국된 상태입니다.", color=0x4000FF)  # 문의 보낸 후 결과 임베드
            await interaction.response.send_message(embed=embed, ephemeral = True)
    if able == False:
        embed = discord.Embed(title="ERROR", description="권한이 없습니다.", color=0x4000FF)  # 문의 보낸 후 결과 임베드
        await interaction.response.send_message(embed=embed, ephemeral = True)

@tree.command(name = '입국거부', description = '가입 대기자의 입국을 거부합니다')  # 문의 명령어
async def slash2(interaction: discord.Interaction, 유저:discord.Member, 사유: str):  # 옵션

    ablerole = get(interaction.user.guild.roles, id=1058613051152150578)
    waitrole = get(interaction.user.guild.roles, id=1058617602517237901)
    able = ablerole in interaction.user.roles
    waitbool = waitrole in 유저.roles

    if able == True:
        if waitbool == True:
            embed = discord.Embed(title="거부 완료", description="ㅤ", color=0x4000FF)  # 문의 보낸 후 결과 임베드
            embed.add_field(name="가입 대기자의 입국을 거부했습니다.", value="ㅤ", inline=False)
            rrole2 = get(interaction.guild.roles, id=1058617602517237901)
            await 유저.remove_roles(rrole2)
            await interaction.response.send_message(embed=embed, ephemeral = True)

            embed1 = discord.Embed(title="명령어 사용 감지됨", description="{} 가 <#{}> 에서 /입국거부 명령어를 사용했습니다.".format(interaction.user.mention, interaction.channel_id), color=0x4000FF)   # 답변 임베드
            ch = client.get_channel(1048251272010158130)
            await ch.send(embed=embed1)
            embed2 = discord.Embed(title="입국이 거부되었습니다.", description="가입지원팀이 당신의 입국을 거부했습니다.", color=0x4000FF)  # 문의 보낸 후 결과 임베드
            embed2.add_field(name="사유 : ", value="`{}`".format(사유), inline=False)
            button1 = Button(label="민원 제기하기", style = discord.ButtonStyle.gray)
            async def button_callback1(interaction: discord.Interaction):
                await interaction.response.send_modal(my_modal())
                md = my_modal()
                embed1 = discord.Embed(title = "입국 거부 민원 접수", description=f"**민원 제기 사유**\n{md.answer}\n\n민원 제기자 : {interaction.user.name}", timestamp = datetime.now(), color=0x4000FF)
                await ch.send(embed=embed1)
            button1.callback = button_callback1
            view = View()
            view.add_item(button1)
            await 유저.send(embed=embed2, view=view)
            await 유저.edit(nick=유저.name)
        if waitbool == False:
            embed = discord.Embed(title="ERROR", description="거부 대상이 입국 요청을 하지 않았거나 입국된 상태입니다.", color=0x4000FF)  # 문의 보낸 후 결과 임베드
            await interaction.response.send_message(embed=embed, ephemeral = True)
    if able == False:
        embed = discord.Embed(title="ERROR", description="권한이 없습니다.", color=0x4000FF)  # 문의 보낸 후 결과 임베드
        await interaction.response.send_message(embed=embed, ephemeral = True)

@tree.command(name = '문의', description = '문의 채널을 생성하여 문의합니다.') 
async def slash2(interaction: discord.Interaction):  # 옵션
    ablerole = get(interaction.user.guild.roles, id=1037736471739768903)
    able = ablerole in interaction.user.roles

    if able == True:
        chname = '『☎️』│ {}님의 문의채널'.format(interaction.user)
        cat = get(interaction.guild.categories, id=1048808664330408017)
        r = get(interaction.guild.roles, id=1037654815171420193)
        ch = await interaction.guild.create_text_channel(chname)
        per = discord.PermissionOverwrite(read_message_history = True, send_messages = True)
        per1 = discord.PermissionOverwrite(read_messages = False)
        await ch.edit(category=cat)
        await ch.set_permissions(target=interaction.user, overwrite=per)
        await ch.set_permissions(target=interaction.guild.default_role, overwrite=per1)
        await ch.set_permissions(target=r, overwrite=per)
        embed2 = discord.Embed(title="문의 채널 생성됨", description="{}님의 문의입니다.".format(interaction.user), color=0x4000FF)  # 문의 보낸 후 결과 임베드
        await ch.send(embed=embed2)
        await ch.send(r.mention)
    if able == False:
        embed = discord.Embed(title="ERROR", description="권한이 없습니다.", color=0x4000FF)  # 문의 보낸 후 결과 임베드
        await interaction.response.send_message(embed=embed, ephemeral = True)

@tree.command(name = '문의종료', description = '문의를 종료합니다.') 
async def slash2(interaction: discord.Interaction):
    ablerole = get(interaction.user.guild.roles, id=1058613051152150578)
    able = ablerole in interaction.user.roles
    yesch = client.get_channel(interaction.channel_id)
    yes = '님의-문의채널' in yesch.name

    if able == True and yes == True:
        await yesch.delete()
    if able == False:
        embed = discord.Embed(title="ERROR", description="권한이 없습니다.", color=0x4000FF)  # 문의 보낸 후 결과 임베드
        await interaction.response.send_message(embed=embed, ephemeral = True)
    if yes == False:
        embed = discord.Embed(title="ERROR", description="문의 종료 명령어는 문의 채널을 제외한 타 채널에서 사용하실 수 없습니다.", color=0x4000FF)  # 문의 보낸 후 결과 임베드
        await interaction.response.send_message(embed=embed, ephemeral = True)

@tree.command(name = '경고수정', description = '플레이어 경고 수를 수정합니다') 
async def slash2(interaction: discord.Interaction, 유저:discord.Member, 수정할경고수: int):
    ablerole = get(interaction.user.guild.roles, id=1058613051152150578)
    able = ablerole in interaction.user.roles
    
    warnbe = {1037736954852290571,1037736958786551839,1037736962112634881,1037736962112634881,1037736965379981353}
    warn = list(warnbe)

    if able == True:
        if 수정할경고수 == 0:
            await 유저.remove_roles (get(interaction.guild.roles, id=warn[0]))
            await 유저.remove_roles (get(interaction.guild.roles, id=warn[1]))
            await 유저.remove_roles (get(interaction.guild.roles, id=warn[2]))
            await 유저.remove_roles (get(interaction.guild.roles, id=warn[3]))
            await 유저.remove_roles (get(interaction.guild.roles, id=warn[4]))
        if not 수정할경고수 == 0:
            await 유저.remove_roles (get(interaction.guild.roles, id=warn[0]))
            await 유저.remove_roles (get(interaction.guild.roles, id=warn[1]))
            await 유저.remove_roles (get(interaction.guild.roles, id=warn[2]))
            await 유저.remove_roles (get(interaction.guild.roles, id=warn[3]))
            await 유저.remove_roles (get(interaction.guild.roles, id=warn[4]))
            await 유저.add_roles (get(interaction.guild.roles, id=warn[수정할경고수]))
    if able == False:
        embed = discord.Embed(title="ERROR", description="권한이 없습니다.", color=0x4000FF)  # 문의 보낸 후 결과 임베드
        await interaction.response.send_message(embed=embed, ephemeral = True)


    

client.run('MTA0NzgxMzI3OTMxMDk0MjIyMA.G4Or5K.jqoqK9wfZTxJB6fOQ8RgICa5REBipOuO1p1RAY') 