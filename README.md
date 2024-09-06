<div align="center">
<img src="https://github.com/CubeGPT/CubeAgents/blob/master/banner.jpeg?raw=true"/>
<img src="https://img.shields.io/badge/Cube-Agents-blue">
<a href="https://github.com/CubeGPT/BuilderGPT/pulls"><img src="https://img.shields.io/badge/PRs-welcome-20BF20"></a>
<img src="https://img.shields.io/badge/License-Apache-red">
<a href="https://discord.gg/kTZtXw8s7r"><img src="https://img.shields.io/discord/1212765516532289587
"></a>
<!-- <p>English | <a href="https://github.com/CubeGPT/CubeAgents/blob/master/README-zh_cn.md">简体中文</a></p> -->
<br>
<a href="https://discord.gg/kTZtXw8s7r">Join our discord</a>
<br/>
</div>

> [!NOTE]
> Developers and translators are welcome to join the CubeGPT Team!

## Introduction
> Give GPT your idea, AI generates customized Minecraft server plugins with one click, which is suitable for Bukkit, Spigot, Paper, Purpur, Arclight, CatServer, Magma, Mohist and other Bukkit-based servers.

BukkitGPT is an open source, free, AI-powered Minecraft Bukkit plugin generator. It was developed for minecraft server owners who are not technically savvy but need to implement all kinds of customized small plugins. From code to build, debug, all done by gpt.

## WebApp
Don't want to prepare the Python & Maven environment? Try our [WebApp](http://cubegpt.org/), designed for non-developers, just enter the plugin name and description, and you can get the plugin jar file.

*The service is paid since the API key we are using is not free. You can get 1 key for 5 generations for $1 [here](https://buymeacoffee.com/baimoqilin/e/293180) or [here (for Chinese users)](https://afdian.com/item/b839835461e311efbd1252540025c377)

## Partner
[![](https://www.bisecthosting.com/partners/custom-banners/c37f58c7-c49b-414d-b53c-1a6e1b1cff71.webp)](https://bisecthosting.com/cubegpt)

## Features

### Core
- Automatically generate code
- Automatically fix bugs
- AI `Better Description`

### GUI
- Creating projects
- Projects management

## Plans and TODOs

Moved to [Projects Tab](https://github.com/orgs/CubeGPT/projects/4).

### Other projects of CubeGPT Team
- [x] Bukkit plugin generator. {*.jar} ([BukkitGPT-v3](https://github.com/CubeGPT/BukkitGPT-v3))
- [ ] Structure generator. {*.schem} (BuilderGPT, or something?)
- [ ] Serverpack generator. {*.zip} (ServerpackGPT or ServerGPT, or..?)
- [ ] Have ideas or want to join our team? Send [us](mailto:admin@baimoqilin.top) an email!

## How it works
When the user types the plugin description, the program lets `gpt-3.5-turbo` optimize the prompt, and then gives the optimized prompt to `gpt-4-turbo-preview`. `gpt-4-turbo-preview` will return it in json format, for example:
```
{
    "output": [
        {
            "file": "%WORKING_PATH%/Main.java",
            "code": "package ...;\nimport org.bukkit.Bukkit;\npublic class Main extends JavaPlugin implements CommandExecutor {\n..."
        },
        {
            "file": "src/main/resources/plugin.yml",
            "code": "name: ...\nversion: ...\n..."
        },
        {
            "file\": "src/main/resources/config.yml",
            "code\": "..."
        },
        {
            "file": "pom.xml",
            "code": "..."
        }
    ]
}
```
The program parses this prompt, copies the entire `projects/template` folder and names it `artifact_name`, and puts the code from the prompt into the each file. Finally the program builds the jar using maven.

## Requirements
You can use BukkitGPT on any computer with [Java](https://www.azul.com/downloads/), [Maven](https://maven.apache.org/), [Python 3+](https://www.python.org/).  

And you need to install this package:
```
pip install openai
```

## Quick Start

*(Make sure you have the [Python](https://www.python.org) environment installed on your computer)*


### Python/UI

1. Download `Source Code.zip` from [the release page](https://github.com/CubeGPT/BukkitGPT-v3/releases) and unzip it.
2. Edit `config.yaml`, fill in your OpenAI Apikey. If you don't know how, remember that [Google](https://www.google.com/) and [Bing](https://www.bing.com/) are always your best friends.
3. Install dependencies by running `pip install -r requirements.txt`.
4. Run `ui.py` (bash `python console.py`).
5. Enter the artifact name & description & package id as instructed to generate your plugin.
6. Copy your plugin from `projects/<artifact_name>/target/<artifact_name>-<version>.jar` to your server `plugins/` folder.
7. Restart your server and enjoy your AI-powered-plugin.

## Troubleshooting

### The POM for org.spigotmc:spigot:jar:1.13.2-R0.1-SNAPSHOT is missing
Solution: [Download BuildTools](https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar), place it in an empty folder, double-click it, choose "1.13.2" in `Settings/Select Version`, click `Compile` in the bottom right corner and let it finish. And then go to your BukkitGPT folder, in `projects/<artifact_name_of_your_plugin>`, double-click `build.bat`. You'll find your plugin in `projects/<artifact_name_of_your_plugin>/target` folder.

## Contributing
If you like the project, you can give the project a star, or [submit an issue](https://github.com/CubeGPT/BukkitGPT-v3/issues) or [pull request](https://github.com/CubeGPT/BukkitGPT-v3/pulls) to help make it better.

## License
```
Copyright [2024] [CubeGPT Team]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
