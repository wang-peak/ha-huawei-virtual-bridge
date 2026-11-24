# Huawei Virtual Bridge

Home Assistant 自定义集成：模拟华为虚拟网关接入华为智慧生活，把 Home Assistant 实体映射为华为智慧生活子设备，支持状态同步与双向控制。支持同时安装多个独立网关实例，彼此互不影响；内置图形化子设备编辑器，可以在 Home Assistant 配置菜单里完成子设备添加、HA 实体绑定与 mapping.yaml 维护。

[![Hassfest](https://github.com/wang-peak/ha-huawei-virtual-bridge/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/wang-peak/ha-huawei-virtual-bridge/actions/workflows/hassfest.yaml)
[![HACS validation](https://github.com/wang-peak/ha-huawei-virtual-bridge/actions/workflows/validate.yaml/badge.svg)](https://github.com/wang-peak/ha-huawei-virtual-bridge/actions/workflows/validate.yaml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

> [!WARNING]
> 本项目是非官方 Home Assistant 自定义集成，未获得华为、OneConnect 项目方或相关平台的官方授权、认可或支持，仅用于技术研究与 Home Assistant 实验环境，请遵守相关平台的服务条款及适用法律。

## 项目来源与二次开发说明

本项目由 **OneConnect Bridge**（[duanyudan86/ha-oneconnect-bridge](https://github.com/duanyudan86/ha-oneconnect-bridge)，Apache License 2.0）二次开发而来，功能与原项目一致：模拟华为网关，把 Home Assistant 实体映射为华为智慧生活虚拟子设备，支持状态同步与双向控制（HA → 华为）。协议栈（CoAP / M2M / SPEKE）、配对流程、子设备映射与持久化实现均沿用原项目。

与原项目相比，当前代码只做了以下调整：

- 集成 domain 由 `oneconnect_bridge` 改为 `huawei_virtual_bridge`，相关线程名与日志文案同步改名。
- 用户界面文案由「OneConnect Bridge」改为「Huawei Virtual Bridge」，并提供英文与简体中文两套 UI 文案（`strings.json`、`translations/en.json`、`translations/zh-Hans.json`）。
- 并入 **OneConnect Bridge GUI**（[wang-peak/ha-oneconnect-bridge-gui](https://github.com/wang-peak/ha-oneconnect-bridge-gui)）的子设备编辑器，作为本集成「配置」菜单（OptionsFlow）的一部分，不再需要单独安装 GUI 集成。
- 补齐 HACS 与 Marketplace 安装所需的打包文件（`hacs.json`、英文翻译等），许可证沿用上游的 Apache License 2.0。
- 适配器扩展：在 `switch` 适配器上补充原项目未注册的开关服务别名，并支持点动服务绑定 `button` 实体（详见下文「适配器扩展」）。

业务逻辑、通信层与 `default_mapping.yaml` 均沿用原项目；适配器集合在上游基础上做了扩展，具体服务与别名见下文「适配器扩展」，逐项修改说明见 [NOTICE](NOTICE)。

## 适配器扩展

在原有适配器集合的基础上，补充了原项目未注册的开关服务别名。支持的服务与别名如下（`inchingSwitch` 可绑定 `button` 实体，其余开关服务只接受 `switch` / `light` / `fan` / `climate` 实体）：

| 服务 | 别名 | 用途 | Profile 自动预填 contract |
| --- | --- | --- | --- |
| `switch` | — | 开关控制：灯、插座、风扇、空调等；绑 `climate` 时用 `on_mode` 决定打开模式 | — |
| `switch` | `switch1`、`switch2`、`switch3`、`switch4` | 多路插排 / 多路开关的分路控制（第 1~4 路） | — |
| `switch` | `usbSwitch1` | 插排的 USB 供电口 | — |
| `switch` | `switchPTC` | 空调电辅热 | — |
| `switch` | `zeroColdSwitch` | 零冷水开关 | — |
| `switch` | `inchingSwitch` | 热水器点动 / 水控零冷水；可绑 `switch` 或 `button`，`on=1` 时触发一次 | — |
| `switch` | `boostMode` | 热水器增压大水量模式 | — |
| `brightness` | — | 灯亮度 | ✅ |
| `cct` | — | 色温（开尔文） | ✅ |
| `colour` | — | 颜色（取 HA light 的 `rgb_color`） | — |
| `mode` | — | 空调模式（`hvac_mode` ↔ Profile 枚举） | ✅ |
| `fan` | — | 空调风速 / 摆风 | ✅ |
| `temperature` | — | 当前 / 目标温度（`sensor` 或 `climate`） | ✅ |
| `humidity` | — | 当前 / 目标湿度（`sensor` 或 `climate`） | ✅ |
| `action` | — | 动作：窗帘开 / 停 / 关、扫地机启动 / 暂停等 | ✅ |
| `action` | `leftAction` | 窗帘左路动作 | ✅ |
| `status` | — | 状态枚举上报（窗帘状态、档位等） | ✅ |
| `status` | `memorySwitch` | 插排断电记忆（0 关 / 1 开 / 2 保持上次） | —（Profile 无 `status` 特性，需手动） |
| `electric` | — | 电量统计（电量 / 电流 / 电压 / 功率） | ✅ |
| `airDetector` | — | 空气检测（温度 + 湿度双 `sensor`） | — |
| `motor` | — | 电机方向 / 开合（窗帘电机） | ✅ |
| `openLevel` | — | 开合度（0~100） | ✅ |
| `opener` | — | 升降开合（0~100） | ✅ |
| `hcho` | — | 甲醛浓度与等级 | — |
| `alarm` | — | 报警（`binary_sensor`） | — |
| `gasSensor` | — | 燃气浓度 | — |
| `cleanerRobot` | — | 扫地机（`vacuum`） | — |
| `power` | — | 功率只读上报（W） | — |

上表的“Profile 自动预填”表示：在编辑器中粘贴设备 Profile JSON 后，编辑器会按 JSON 中的特性枚举与取值范围自动预填该服务的 contract；标 — 的服务需要手动填写（留空也可）。使用预置产品模板时，模板自带的 contract 同样会自动预填；`action` 需同设备存在 `motor` / `openLevel` / `opener` / `status` 或 `switch` 才能判定动作角色，`temperature` / `humidity` 仅按 Profile 中出现的当前值与目标值特性预填。


## 安装方式

### 通过 Home Assistant Marketplace 安装（推荐，Home Assistant 2026.11 及以上）

Home Assistant 2026.11 起 Marketplace 已内置于 Home Assistant（即内置的 HACS），可在 **设置 → Marketplace** 打开，无需再单独安装 HACS。

1. 进入 **设置 → Marketplace**，点击右上角的 **Add from link**（通过链接添加）。
2. 在 **GitHub link** 中填写完整仓库地址 `https://github.com/wang-peak/ha-huawei-virtual-bridge`（也可以填 `wang-peak/ha-huawei-virtual-bridge`），选择 **Add**。若 Marketplace 无法自动识别内容类型，在 **Type** 中选择 **集成（Integration）** 后再次选择 **Add**。
3. 首次添加自定义仓库时，Marketplace 会提示先连接 GitHub 账号；该连接只读取公开信息，不会申请私有仓库权限，也不会申请修改权限。
4. 在仓库列表中选择 **Huawei Virtual Bridge**，进入详情页后点击安装。
5. 重启 Home Assistant，进入 **设置 → 设备与服务 → 添加集成**，搜索 **Huawei Virtual Bridge** 并按提示配对。


<!-- ha-marketplace:exclude-start -->

### 通过 HACS 安装（Home Assistant 2026.11 之前的版本）

1. 在 Home Assistant 中打开 **HACS** → **集成（Integrations）**。
2. 点击右上角 **+** 按钮，选择 **自定义仓库（Custom repositories）**。
3. 仓库 URL 填写：`https://github.com/wang-peak/ha-huawei-virtual-bridge`
4. 类别选择 **集成（Integration）**，点击添加。
5. 在 HACS 集成列表中找到 **Huawei Virtual Bridge**，点击 **下载（Download）**。
6. 重启 Home Assistant，进入 **设置 → 设备与服务 → 添加集成**，搜索 **Huawei Virtual Bridge** 并按提示配对。

<!-- ha-marketplace:exclude-end -->

### 手动安装

1. 下载本仓库源码，将 `custom_components/huawei_virtual_bridge/` 目录完整拷贝到 Home Assistant 配置目录下的 `custom_components/` 中，即：

   ```
   config/custom_components/huawei_virtual_bridge/
   ```

   也可以直接下载 Release 附件 `ha-huawei-virtual-bridge.zip` 并解压到 Home Assistant 配置目录；包内只有 `custom_components/huawei_virtual_bridge/`，不会向配置目录散落其他文件。

2. 重启 Home Assistant。
3. 进入 **设置 → 设备与服务 → 添加集成**，搜索 **Huawei Virtual Bridge** 并按提示配对。

## 配置

添加集成时需要：

- **配对网卡 IPv4 地址**：本机用于与 Huawei 网关局域网通信的 IPv4 地址。
- **PIN 码**：在华为智慧生活 App 中添加网关时显示的 8 位 PIN，手动输入完成配对。

添加完成后，可在 **设置 → 设备与服务 → Huawei Virtual Bridge → 配置** 打开子设备编辑器（OptionsFlow），菜单包含：

- **配对网络接口**：更换虚拟网关监听的 IPv4 网卡（会重载该网关入口）。
- **添加子设备（含实体绑定）**：从 10 个华为预置产品模板中选择，或粘贴设备 Profile JSON 自动识别产品参数；随后逐个华为服务选择对应的 HA 实体并填写 contract（可选）。
- **编辑子设备与实体**、**删除子设备**：修改或删除已注册的虚拟子设备。
- **直接编辑 YAML**：直接编辑该网关的 `mapping.yaml`（保存前按本集成规则校验，并保留 `.bak` 备份）。
- **启用或停用映射**：停用会从华为云端移除已注册子设备，启用后重新注册。各项保存后都会自动重载；需要手动重载时，可使用设备页上的“重载子设备”按钮。

实体绑定规则：开关类服务（`switch`、`switch1`~`switch4`、`switchPTC` 等）绑定 `switch` / `light` / `fan` / `climate` 实体；只有点动服务 `inchingSwitch` 允许绑定 `button` 实体（云端 `on=1` 时触发一次 `button.press`），其它服务绑定 `button` 会在保存时被拒绝。

编辑器只读写本集成自己的 `mapping.yaml`（`config/.storage/huawei_virtual_bridge/gateways/<serial>/mapping.yaml`），不修改原 OneConnect Bridge 的任何文件。界面文案支持英文与简体中文（跟随 Home Assistant 语言）。

## 多实例并存

本集成支持在同一 Home Assistant 实例中同时安装多个网关入口，每个入口使用独立的 `serial` 标识，实体 ID、设备注册、通知 ID 均相互隔离，互不影响。

如需与原 OneConnect Bridge 集成共同安装，请保留原 `custom_components/oneconnect_bridge/` 目录，本集成作为独立的第二个集成并行使用，两者 domain 均不同，不会冲突。

## 文件结构

```
ha-huawei-virtual-bridge/
├── hacs.json                       # HACS / Marketplace 仓库清单（名称、最低 HA 版本）
├── README.md                       # 项目说明（HACS / Marketplace 展示页）
├── LICENSE                         # Apache License 2.0（沿用上游项目许可证）
├── NOTICE                          # 上游来源、二次开发与修改说明
└── custom_components/huawei_virtual_bridge/
    ├── manifest.json               # 集成清单（domain、version、categories、requirements）
    ├── strings.json                # 英文 UI 字符串源文件
    ├── translations/
    │   ├── en.json                 # 英文 UI 字符串
    │   └── zh-Hans.json            # 中文 UI 字符串
    ├── config_flow.py              # 配置流程（网卡配对）与 OptionsFlow 菜单入口
    ├── const.py                    # 常量定义（DOMAIN 等）
    ├── __init__.py                 # 集成入口（async_setup / async_setup_entry）
    ├── gateway.py                  # 网关管理与云端连接
    ├── entity.py                   # 实体基类
    ├── binary_sensor.py            # 二传感器平台
    ├── sensor.py                   # 传感器平台
    ├── button.py                   # 按钮平台
    ├── ha_adapter.py               # HA 实体适配器
    ├── storage.py                  # 本地持久化存储
    ├── default_mapping.yaml        # 默认子设备映射
    ├── business/                   # 子设备业务逻辑（映射、协议、清理等）
    ├── core/                       # 核心通信层（CoAP、M2M、配对运行时等）
    ├── child_ui/                   # 图形化子设备编辑器（OptionsFlow 菜单）
    │   ├── flow.py                 # 编辑流程：模板/Profile、逐服务实体绑定、YAML 编辑、启停
    │   ├── profile.py              # mapping.yaml 读写、校验与 .bak 备份
    │   ├── runtime.py              # 保存后重载网关入口
    │   ├── product_templates.py    # 华为预置产品模板（9MU7 / 9MXO / 9MY5 等）
    │   ├── services_catalog.py     # 华为服务目录（20 个 sid 与 contract 说明）
    │   ├── contract_fields.py      # contract 字段中英文对照
    │   ├── device_profile.py       # 设备 Profile JSON 解析
    │   ├── mapping_ops.py          # 子设备条目的增删改
    │   ├── __init__.py             # 编辑器包说明
    │   └── const.py                # 编辑器常量与菜单项
    └── brand/icon.png              # 集成图标（HACS / Marketplace 品牌资产）
```

## 依赖

- `psutil>=5.9.0`

`cryptography` 由 Home Assistant 自身提供，无需在本集成中声明。

依赖会在 HACS / Marketplace 或手动安装集成后由 Home Assistant 自动安装。本集成要求 Home Assistant **2024.12.0** 及以上。

## 问题反馈

- 问题跟踪：https://github.com/wang-peak/ha-huawei-virtual-bridge/issues
- 文档：https://github.com/wang-peak/ha-huawei-virtual-bridge

## 许可证

本项目采用 [Apache License 2.0](LICENSE) 许可证。

本项目由 [OneConnect Bridge](https://github.com/duanyudan86/ha-oneconnect-bridge)（Apache License 2.0）二次开发而来，来源、版权与逐项修改说明见 [NOTICE](NOTICE)，二次开发概述见上文「项目来源与二次开发说明」。
