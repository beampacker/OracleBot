import discord
from discord.ext import commands
from discord import app_commands
from prop_logic import calculate_proj
from config import BOT_TOKEN, ODDS_API_KEY

intents = discord.Intents.default()
intents.message_content = False

bot = commands.Bot(command_prefix="!", intents=intents)

class OracleBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="prop", description="Analyze an NBA prop using OracleBot AI.")
    @app_commands.describe(
        player="Player name",
        stat="Stat type (PTS, REB, AST, PRA, RA, PR, 3PT)",
        line="Prop line number",
        opponent="Opponent team abbreviation (ex: BOS, LAL, DAL)",
        homeaway="Home or Away (H/A)"
    )
    async def prop(
        self,
        interaction: discord.Interaction,
        player: str,
        stat: str,
        line: float,
        opponent: str,
        homeaway: str
    ):
        await interaction.response.defer()

        data = calculate_proj(player, stat, line, opponent, homeaway)

        embed = discord.Embed(
            title=f"{player} — {stat} {line}",
            description=f"Oracle Analysis for **{player}**",
            color=0x00ffaa
        )

        embed.add_field(name="Weighted Projection", value=data["weighted"], inline=True)
        embed.add_field(name="Final Projection", value=data["projection"], inline=True)
        embed.add_field(name="Difference vs Line", value=data["difference"], inline=True)

        embed.add_field(name="Recommendation", value=data["recommendation"], inline=False)

        embed.add_field(name="DVP Rank", value=data["dvp_rank"], inline=True)
        embed.add_field(name="Pace", value=data["pace"], inline=True)

        await interaction.followup.send(embed=embed)

    async def cog_load(self):
        print("OracleBot Loaded.")

@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print("Slash commands synced.")
    except Exception as e:
        print("Error syncing:", e)

    print(f"Logged in as {bot.user}")

bot.add_cog(OracleBot(bot))
bot.run(BOT_TOKEN)
