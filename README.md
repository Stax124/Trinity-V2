<div id="top"></div>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Stax124/Trinity-V2">
    <img src="img/Trinity-V2.png" alt="Logo" height="200">
  </a>

<h2 align="center">Trinity V2</h2>

  <p align="center">
    Powerful discord bot for handling economy and wars for Discord servers
    <br />
    <a href="https://github.com/Stax124/Trinity-V2/issues">Report Bug</a>
    ·
    <a href="https://github.com/Stax124/Trinity-V2/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#commands">Commands</a>
      <ul>
        <li><a href="#extensions">Extensions</a></li>
        <li><a href="#battle">Battle</a></li>
        <li><a href="#config">Config</a></li>
        <li><a href="#essentials">Essentials</a></li>
        <li><a href="#expeditions">Expeditions</a></li>
        <li><a href="#fallback">Fallback</a></li>
        <li><a href="#income">Income</a></li>
        <li><a href="#inventory">Inventory</a></li>
        <li><a href="#management">Management</a></li>
        <li><a href="#money">Money</a></li>
        <li><a href="#owner">Owner</a></li>
        <li><a href="#player">Player</a></li>
        <li><a href="#playershop">PlayerShop</a></li>
        <li><a href="#settings">Settings</a></li>
        <li><a href="#work">Work</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

Trinity is a discord bot that changes your server to both an economy and a roleplay server (if you choose to use it). Filled with fully operational battle mechanics, quests, items to horde, shop and leveling system, you will be ready to trade, conquer and raid your opponents.

**This bot allows you to hot-swap all of the modules on the fly, and it is also fully customizable. Feel free to take advantage of the features and add your own.**

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

- [Discord.py](https://github.com/Rapptz/discord.py)
- [Discord-pretty-help](https://github.com/stroupbslayen/discord-pretty-help)
- [DiscordUtils](https://github.com/toxicrecker/DiscordUtils)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get this bot up and running, follow these steps.

### Prerequisites

- python (3.9 tested, might run on older versions)
  ```sh
  sudo apt install python3 pip3
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Stax124/Trinity-V2
   ```
2. Install requirements
   ```sh
   pip3 install -r requirements.txt
   ```
3. Enter your Discord API token (optionally, pass it as an argument on runtime with `--token your_token_here`)
   ```sh
   export TRINITY="your_token_here"
   ```
4. Run the bot
   ```sh
   python3 main.py [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-f FILE] [--token TOKEN]
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Commands

### Extensions

```
load <cog: string> - Loads extension
reload <cog: string> - Reloads extension
reload-all - Reloads all extensions
unload <cog: string> - Unloads extension
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Battle

```
attack <player_manpower: int> - Automatized battle system
manpower - Show manpower of user
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Config

```
config <path: str> [path: str]... - Output config as browsable directory
config-load - loads config file for current server
config-save - saves config file for current server
set <path: str> [path: str]... { = | < | > } <value> - Change values in config ("<" = subtraction | ">" = addition). You rather know what ya doin! (This can break the config when you do it wrong)
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Essentials

```
autorole <role: discord.Role> - Set default role for new members
limits - Shows upgrade limits for your account
members - Show all members
purge <number: int> - Delete messages from channel
role - Shows your roles
roles - Shows all roles
roll <sides: int> - Roll a dice
time - shows time as bot sees it (for timezone purposes)
upgrades - Shows the current number of upgrades bought
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Expeditions

```
add-expedition [-h] [--manpower MANPOWER] [--level LEVEL] [--chance CHANCE] [--common COMMON] [--uncommon UNCOMMON] [--rare RARE] [--epic EPIC] [--legendary LEGENDARY] [--xp XP] [--description DESCRIPTION] name cost hours - Adds new expedition
expedition <name: str> - Starts selected expedition
expeditions - Shows all expeditions
remove-expedition <name: str> - Removes selected expedition
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Fallback

```
fallback-load - Loads fallback config
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Income

```
add-income <role: discord.Role> <value: integer>
income - Shows your income
income-calc <population: int> - Calculates income from population number
income-lb - Shows the income leaderboard (aliases: l, lb, leaderboard)
remove-income <role: discord.Role> <value: integer> - Remove income from role
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Inventory

```
add-player-item UNION[str, discord.Member] [--income INCOME] [--income_percent INCOME_PERCENT] [--discount DISCOUNT] [--discount_percent DISCOUNT_PERCENT] [--description DESCRIPTION] name {common,uncommon,rare,epic,legendary,event} {helmet,weapon,armor,leggins,boots,artefact} - Adds new item to player's inventory
equip <item: str> - Equips item
equiped - Shows all equiped items
inventory - Shows your "Realy useful" items in your inventory
recycle <item: str> - Recycles item from your inventory
recycle-all <rarity: str> - Recycles all items of selected rarity
remove-player-item <user: Union[str, discord.Member]> <item: str> - Removes item from player's inventory
unequip <item: str> - Unequips item
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Management

```
ban <user: discord.Member> - Bans selected user
kick <user: discord.Member> - Kicks selected user
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Money

```
add-money <user: discord.Member> <value: integer> - Adds money to user
balance - Shows your balance
buy <type: str> <value: int> - Spend money to make more money
leaderboard - Shows how poor you are
pay <user: discord.Member> <value: int> - Self-explanatory
remove-money <user: discord.Member> <value: integer> - Removes money from user
reset-money <user: discord.Member> - Resets user's balance
shop - Shows all items that you are too poor to buy
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Owner

```
asyncs-on-hold - Show active async jobs that are in queue
eval - Evaluates code
exec - Executes code
shutdown - Shuts down the bot
tclear - Clears terminal screen
update - Updates the bot (requires git and no modifications done)
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Player

```
level - Shows your level and xp progress
levelup <skill: str> [value: int = 1] - Levels up a skill
skillpoints - Shows number of your skillpoints remaining
talents - Shows your skills
```

<p align="right">(<a href="#top">back to top</a>)</p>

### PlayerShop

```
player-buy <user: discord.Member> <item: str> - Buys item from player
player-retrieve <item: str> - Removes listing and puts item back to your inventory
player-sell <price: int> <item: str> - Puts item on sale
player-shop <player: discord.Member> - Shows all items player is selling
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Settings

```
add-item [--maxupgrade MAXUPGRADE] [--income INCOME] [--manpower MANPOWER] [--require REQUIRE] name cost - Adds item to database
deltatime <value: int> -  Sets time between work commands
pause - Pauses everything (except unpause)
version - Shows current version of bot
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Work

```
work - What are you doing, make some money!
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what makes the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Tomáš Novák - tamoncz@gmail.com

Project Link: [https://github.com/Stax124/Trinity-V2](https://github.com/Stax124/Trinity-V2)

<p align="right">(<a href="#top">back to top</a>)</p>

[contributors-shield]: https://img.shields.io/github/contributors/Stax124/Trinity-V2.svg?style=for-the-badge
[contributors-url]: https://github.com/Stax124/Trinity-V2/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Stax124/Trinity-V2.svg?style=for-the-badge
[forks-url]: https://github.com/Stax124/Trinity-V2/network/members
[stars-shield]: https://img.shields.io/github/stars/Stax124/Trinity-V2.svg?style=for-the-badge
[stars-url]: https://github.com/Stax124/Trinity-V2/stargazers
[issues-shield]: https://img.shields.io/github/issues/Stax124/Trinity-V2.svg?style=for-the-badge
[issues-url]: https://github.com/Stax124/Trinity-V2/issues
[license-shield]: https://img.shields.io/github/license/Stax124/Trinity-V2.svg?style=for-the-badge
[license-url]: https://github.com/Stax124/Trinity-V2/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/tom%C3%A1%C5%A1-nov%C3%A1k-5a163321b/
[product-screenshot]: images/screenshot.png
