import io

import discord
from PIL import Image, ImageDraw, ImageFont, ImageOps

from bot.emojis import Emojis
from bot.functions import create_embed, escape_markdown
from data.useful import Ids


async def member_join(self: discord.Client, member: discord.Member):
    if member.guild.id == Ids["Support_server"]:
        if Ids["Member_role"] and not member.bot:
            member_role = member.guild.get_role(Ids["Member_role"])
            await member.add_roles(member_role)

        users = 0
        for m in member.guild.members:
            if not m.bot:
                users += 1
        for channel in member.guild.channels:
            if channel.name.startswith("👤 "):
                await channel.edit(name=f"👤 Users: {users: ,}")
                break
        else:
            overwrite = {member.guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=True)}
            await member.guild.create_voice_channel(f"👤 Users: {users: ,}", overwrites=overwrite)

        buffer_avatar = io.BytesIO()
        await member.display_avatar.save(buffer_avatar)
        buffer_avatar.seek(0)

        avatar = Image.open(buffer_avatar).convert("RGBA")
        avatar = avatar.resize((512, 512))
        bigsize = (avatar.size[0] * 3, avatar.size[1] * 3)
        mask = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask)

        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mask)

        output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)

        avatar_image = output
        avatar_size = 768
        avatar_image = avatar_image.resize((avatar_size, avatar_size))

        image = Image.open("ressources/welcome.png")
        image = image.resize((1920, 1080))
        image_width, image_height = image.size
        foreground = avatar_image
        x = (1024 - avatar_size) // 2
        y = (image_height - avatar_size) // 2
        image.paste(foreground, (x, y), foreground)

        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype("ressources/supercell_magic_webfont.ttf", 100)
        text_width, text_height = draw.textsize(f"Welcome {member.name}", font=font)
        x = (image_width - text_width) // 2
        y = (image_height - text_height) // 2 - 400
        text_color = (55, 115, 235)
        draw.text((x, y), f"Welcome {member.name}", fill=text_color, font=font)
        text_width, text_height = draw.textsize("Clash INFO support server", font=font)
        x = (image_width - text_width) // 2
        y = (image_height - text_height) // 2 + 400
        draw.text((x, y), "Clash INFO support server", fill=text_color, font=font)

        buffer_output = io.BytesIO()
        image.save(buffer_output, format="PNG")
        buffer_output.seek(0)
        file = discord.File(buffer_output, "Welcome.png")
        url = "attachment://Welcome.png"

        rules_channel = member.guild.get_channel(Ids["Rules_channel"])
        embed = create_embed(f"Welcome {escape_markdown(member.name)} !", f"Welcome ! Please check the {rules_channel.mention}, you will find everything you need here !\n{Emojis['Id']} ID: `{member.id}`\n{Emojis['Discord']} Discord account creation: {member.created_at.date().isoformat()}", member.color, "", member.guild.me.display_avatar.url, img=url)
        welcome = member.guild.get_channel(Ids["Welcome_channel"])
        await welcome.send(embed=embed, file=file)
    return
