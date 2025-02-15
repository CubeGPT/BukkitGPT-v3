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
> Give the LLM your idea, AI generates customized Minecraft server plugins with one click, which is suitable for Bukkit, Spigot, Paper, Purpur, Arclight, CatServer, Magma, Mohist and other Bukkit-based servers.

BukkitGPT is an open source, free, AI-powered Minecraft Bukkit plugin generator. It was developed for minecraft server owners who are not technically savvy but need to implement all kinds of customized small plugins. From code to build, debug, all done by the LLM.

## WebApp

> [!WARNING]
> There're big differences between *BukkitGPT(-v3)* and *BukkitGPT WebApp*. The BukkitGPT is a self-hosted, free, open-source, community-driven project, while the BukkitGPT WebApp is a paid, cloud-hosted service that provides a more user-friendly experience for non-developers.
> Issues and questions about BukkitGPT WebApp should be directed to our [Discord Server](https://discord.gg/kTZtXw8s7r).

Don't want to deal with Python, Maven, BuildTools, and other complicated environments?
Hey! Here's [the WebApp version](https://webapp.cubegpt.org) designed just for you - generate plugins **even on your phone**!

*The service is paid since the API key we are using is not free. You can get 1 key for 5 generations for $1 [here](https://ko-fi.com/s/cd5d4fcaba) or [here (for Chinese users)](https://afdian.com/item/b839835461e311efbd1252540025c377)

*The WebApp edition doesn't support plugin editing feature yet, but we are working on it.
</details>

## Features

- Automatically generate plugin code based on the user's description.
- Edit existing plugins.

### Other projects of CubeGPT Team
- [x] Bukkit plugin generator. {*.jar} ([BukkitGPT-v3](https://github.com/CubeGPT/BukkitGPT-v3))
- [x] Structure generator. {*.schem} ([BuilderGPT](https://github.com/CubeGPT/BuilderGPT))
- [ ] Serverpack generator. {*.zip} (ServerpackGPT or ServerGPT, or..?)
- [ ] Have ideas or want to join our team? Send [us](mailto:admin@baimoqilin.top) an email!

## Requirements
You can use BukkitGPT on any computer with [Java](https://www.azul.com/downloads/), [Maven](https://maven.apache.org/), [Python 3+](https://www.python.org/) **AND** [BuildTools](https://github.com/CubeGPT/BukkitGPT-v3#the-pom-for-orgspigotmcspigotjar1132-r01-snapshot-is-missing) installed. 

## Quick Start

1. Clone the repository and install the dependencies with command:
```bash
git clone https://github.com/CubeGPT/BukkitGPT-v3
cd BukkitGPT-v3
python -m venv venv
source venv/bin/activate # for Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```
2. Edit `config.yaml` and fill in your OpenAI API Key.
3. Run `ui.py` (with command `python ui.py`).
4. Enjoy!

## Troubleshooting

### The POM for org.spigotmc:spigot:jar:1.13.2-R0.1-SNAPSHOT is missing
1. [Download BuildTools](https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar) and place it in *an empty folder*.
2. Open the file.
3. Choose `1.13.2` in `Settings/Select Version`.
4. Click `Compile` in the bottom right corner and let it finish.
5. Go to your BukkitGPT folder, execute `build.bat` in `projects/<artifact_name_of_your_plugin>`.
6. You'll find your plugin in `projects/<artifact_name_of_your_plugin>/target` folder.

## Contributing
If you like the project, you can give the project a star, or [submit an issue](https://github.com/CubeGPT/BukkitGPT-v3/issues) or [pull request](https://github.com/CubeGPT/BukkitGPT-v3/pulls) to help make it better.

## Credits

- [Isaac Turner](https://github.com/noporpoise)'s [unifieddiff.py](https://gist.github.com/noporpoise/16e731849eb1231e86d78f9dfeca3abc), we use it to apply diffs to the files.

- [QGUI](https://github.com/QPT-Family/QGUI), the UI framework used in `ui.py`.

- [CFR](https://github.com/leibnitz27/cfr), the decompiler used for the plugin editing feature.

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
