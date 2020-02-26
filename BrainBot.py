import discord
from discord.ext import commands
from random import choice
from os import listdir


class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("----------\nLogged in as:\n{0}\n{1}\n----------".format(self.bot.user.name, self.bot.user.id))

    @commands.command(name="help", aliases=["h"])
    async def help(self, ctx, *args):
        await ctx.message.delete()

        main_embed = discord.Embed(title="__**Help Commands**__", colour=0x00ff00)
        main_embed.add_field(name="**Command Help**",
                             value="Remind me to do stuff here. Also *execute <code>, *settings and *help are all the "
                                   "current commands",
                             inline=False)
        help_message = await ctx.send(embed=main_embed)

        await help_message.add_reaction("<:cross:671116183780720670>")

        def check(reaction, user, *args):
            return str(reaction) == "<:cross:671116183780720670>" and str(reaction.message) == str(
                help_message) and user != reaction.message.author

        await self.bot.wait_for("reaction_add", check=check)
        await help_message.delete()

    @commands.command(name="settings", aliases=["setting", "s"])
    async def settings(self, ctx, *args):
        """
        :param ctx: Discord Context class
        :param args: Any additional args in the command

        :var settings_embed: Discord embed class for the settings output
        :var settings_message: Discord message class containing settings_embed
        :var home_page: Bool for logic on whether the home page should be displayed
        :var id_reaction_list: List of reactions
        """
        await ctx.message.delete()
        home_page = True

        settings_embed = discord.Embed(title="**Settings**", colour=0x9966ff)
        settings_embed.add_field(name="\u200b",
                                 value="\u200b",
                                 inline=False)
        settings_message = await ctx.send(embed=settings_embed)

        string_reaction_list = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "◀️", "<:cross:671116183780720670>"]

        def check(reaction, user, *args):
            id_reaction_list = ["<:cross:671116183780720670>",
                                "\u0031\ufe0f\u20e3",
                                "\u0032\ufe0f\u20e3",
                                "\u0033\ufe0f\u20e3",
                                "\u0034\ufe0f\u20e3",
                                "\u0035\ufe0f\u20e3",
                                "\u25c0\ufe0f"]

            return (str(reaction) in id_reaction_list) and \
                   (str(reaction.message) == str(settings_message)) and \
                   (user != reaction.message.author)

        while True:
            if home_page:
                settings_embed.set_field_at(index=0,
                                            name="**Options:**",
                                            value="<Placeholder for info on settings>\n**1.** Cell Size\n**2.** "
                                                  "Character Set\n**3.** Console Line Output",
                                            inline=False)
                await settings_message.edit(embed=settings_embed)
                await settings_message.add_reaction("\u0031\ufe0f\u20e3")
                await settings_message.add_reaction("\u0032\ufe0f\u20e3")
                await settings_message.add_reaction("\u0033\ufe0f\u20e3")
                await settings_message.add_reaction("<:cross:671116183780720670>")

                reaction, user = await self.bot.wait_for("reaction_add", check=check)
                await settings_message.clear_reactions()

            if str(reaction.emoji) == "<:cross:671116183780720670>":
                await settings_message.delete()

            if str(reaction.emoji) in string_reaction_list:
                home_page = False

                if str(reaction.emoji) == "1️⃣":
                    settings_embed.set_field_at(index=0, name="**Cell Size:**",
                                                value="1. 8 bit [Recommended]\n2. 16 bit\n3. 32 bit\n4. 64 bit\n5. "
                                                      "Dynamic (Unlimited)",
                                                inline=False)
                    await settings_message.edit(embed=settings_embed)
                    await settings_message.add_reaction("\u0031\ufe0f\u20e3")
                    await settings_message.add_reaction("\u0032\ufe0f\u20e3")
                    await settings_message.add_reaction("\u0033\ufe0f\u20e3")
                    await settings_message.add_reaction("\u0034\ufe0f\u20e3")
                    await settings_message.add_reaction("\u0035\ufe0f\u20e3")
                    await settings_message.add_reaction("\u25c0\ufe0f")
                    await settings_message.add_reaction("<:cross:671116183780720670>")

                    reaction, user = await self.bot.wait_for("reaction_add", check=check)

                elif str(reaction.emoji) == "2️⃣":
                    settings_embed.set_field_at(index=0, name="**Character Set:**",
                                                value="1. ASCII [Recommended]\n2. Unicode",
                                                inline=False)
                    await settings_message.edit(embed=settings_embed)
                    await settings_message.add_reaction("\u0031\ufe0f\u20e3")
                    await settings_message.add_reaction("\u0032\ufe0f\u20e3")
                    await settings_message.add_reaction("\u25c0\ufe0f")
                    await settings_message.add_reaction("<:cross:671116183780720670>")

                    reaction, user = await self.bot.wait_for("reaction_add", check=check)

                elif str(reaction.emoji) == "3️⃣":
                    settings_embed.set_field_at(index=0, name="**Console Line Output:**",
                                                value="1. On\n2. Off",
                                                inline=False)
                    await settings_message.edit(embed=settings_embed)
                    await settings_message.add_reaction("\u0031\ufe0f\u20e3")
                    await settings_message.add_reaction("\u0032\ufe0f\u20e3")
                    await settings_message.add_reaction("\u25c0\ufe0f")
                    await settings_message.add_reaction("<:cross:671116183780720670>")

                    reaction, user = await self.bot.wait_for("reaction_add", check=check)

                if str(reaction.emoji) == "◀️":
                    home_page = True

                await settings_message.clear_reactions()

    @commands.command(name="execute", aliases=["exe", "e"])
    async def execute(self, ctx, *args):
        """
        :param ctx: Discord Context class
        :param code_string: String code to be executed by the interpreter
        :param args: Any additional args in the command

        :var out_console_embed: Discord embed class for the console output
        :var out_console_message: Discord message class containing out_console_embed
        :var out_console_field_val: String field value for out_console_embed

        :var sys_console_embed: Discord embed class for the error output
        :var sys_console_message: Discord message class containing sys_console_embed
        :var sys_console_field_val: String field value for sys_console_embed

        :var input_info_message: Discord message class containing the input request message
        :var user_inp_message: Discord message class containing the users input message

        :var stack: Array representation of the memory stack
        :var loops: Array holding loop locations for loop logic
        :var pointer: Integer value for the current memory address
        :var pc: Integer value for the current line of code [program counter]
        """

        await ctx.message.delete()

        executer = ctx.message.author.id
        out_console_field_val = "```"
        sys_console_field_val = ""

        code_string = "".join(args)

        # Console embed initialisation
        out_console_embed = discord.Embed(title="**Brainfuck Console**", name="**Code Output**", colour=0x3DE1FF)
        out_console_embed.add_field(name="**Code output**", value="None", inline=False)
        out_console_message = await ctx.send(embed=out_console_embed)

        # Error embed initialisation
        sys_console_embed = discord.Embed(title="**Error Log**", colour=0xFF002A)
        sys_console_embed.add_field(name="**Error output**", value="None", inline=False)
        sys_console_message = await ctx.send(embed=sys_console_embed)

        if code_string == "":
            sys_console_field_val += "**Error** Enter a string of instructions to be executed\n"
            sys_console_embed.set_field_at(index=0, name="**Error output**", value=sys_console_field_val, inline=False)
            await sys_console_message.edit(embed=sys_console_embed)
        else:
            code_string = code_string.replace("\n", "")
            stack = [0] * 30000  # Memory
            loops = []  # Loops
            pointer = 0  # Memory Counter
            pc = 0  # Program Counter

            # Interpreter
            while pc < len(code_string):
                if code_string[pc] == "+":  # Increment
                    stack[pointer] += 1

                elif code_string[pc] == "-":  # Decrement
                    stack[pointer] -= 1

                elif code_string[pc] == "<":  # Move pointer left
                    pointer -= 1

                elif code_string[pc] == ">":  # Move pointer right
                    pointer += 1

                elif code_string[pc] == ".":  # Output memory val as char
                    if stack[pointer] == 92:  # Fixing escape code issue
                        out_console_field_val += "\\"
                    else:
                        out_console_field_val += chr(stack[pointer])

                elif code_string[pc] == ",":  # Input char as val
                    input_info_message = await ctx.send("Do *input <char>")
                    while True:
                        user_inp_message = await self.bot.wait_for("message")

                        # Valid input cmd
                        if user_inp_message.content[:6] == "*input" or user_inp_message.content[:3] == "*i":
                            # chars = 1
                            if len(user_inp_message.content[7:]) == 1:
                                stack[pointer] = ord(user_inp_message.content[7])
                                break

                            # chars = 1
                            elif len(user_inp_message.content[3:]) == 1:
                                stack[pointer] = ord(user_inp_message.content[3])
                                break

                            # chars != 1
                            else:
                                sys_console_field_val += "**Error** Input only takes a single character\n"
                                sys_console_embed.set_field_at(index=0, name="**Error output**", value=sys_console_field_val,
                                                         inline=False)
                                await sys_console_message.edit(embed=sys_console_embed)

                        # Deleting message if input
                        if user_inp_message.content[:6] == "*input" or user_inp_message.content[:2] == "*i":
                            await user_inp_message.delete()

                    await input_info_message.delete()

                elif code_string[pc] == "[":  # Loop start
                    loops.append(pc)

                elif code_string[pc] == "]":  # Loop end
                    if stack[pointer] != 0:
                        pc = loops[-1]
                    else:
                        del loops[-1]

                else:  # Illegal value
                    sys_console_field_val += "**Error** Ignored invalid instruction '" + code_string[pc] + "'\n"
                    sys_console_embed.set_field_at(index=0, name="**Error output**", value=sys_console_field_val, inline=False)
                    await sys_console_message.edit(embed=sys_console_embed)
                pc += 1

            out_console_field_val += "```"
            if out_console_field_val == "``````":
                out_console_field_val = "None"

            out_console_embed.set_field_at(index=0, name="**Code output**", value=out_console_field_val, inline=False)
            await out_console_message.edit(embed=out_console_embed)

    @commands.command(name="input", aliases=["i"])
    async def null_commands(self, *args):
        pass


bf = commands.Bot(command_prefix="*", description="Brainfuck time")
bf.remove_command("help")
bf.add_cog(MainCog(bf))
bf.run(open("token.secret", "r").read())
