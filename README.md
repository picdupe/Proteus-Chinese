# Proteus Chinese

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)]()
[![Version](https://img.shields.io/badge/version-9.1%20SP2%20Build%2042460-orange.svg)]()   
**高质量的 Proteus 汉化包**   
*让 Proteus 更贴近中文用户！*

---

## 项目简介

Proteus Chinese 是一个专业的 Proteus 软件汉化项目。通过结合百度翻译 API 的自动化翻译与专业人工后期校对，我们致力于为用户提供媲美原生中文体验的高质量汉化版本。

### 项目特色

- **智能初译**：利用百度翻译 API 进行高效准确的初步翻译
- **人工精校**：专业团队对自动化翻译结果进行逐句优化
- **术语统一**：建立专业术语库，确保翻译一致性
- **体验优化**：深度适配中文用户使用习惯
- **持续更新**：跟随 Proteus 版本更新同步维护

## 项目目标

- 提供完整、准确、自然的 Proteus 中文界面
- 消除语言障碍，降低国内用户学习门槛
- 建立规范的电子设计自动化（EDA）软件汉化标准
- 打造开源汉化社区的典范项目

---

## 项目背景

### 1. **为什么做这个汉化包？**

- 我在学习单片机时需要使用 Proteus，但是搜遍互联网只找到 `广州市风标电子技术有限公司` 制作的 Proteus 汉化语言包（该公司名称是从汉化包中发现的，制作者不确定是不是这个公司），各种教程都使用这个2014年发布的老汉化语言包，现在词条已经增加到了1万多条，而这个汉化语言包仅有4000条可用，且很多上下文也已经改变，实际可用词条可能只有几百条。
- 为了让更多中文用户能够更方便地使用这款软件，我决定制作这个汉化包。

### 2. **翻译质量如何？**

- 使用 **百度翻译 API ** 进行初步翻译。
- 结合后期人工矫正，确保翻译结果准确、自然。
- 这是市面上翻译质量最高的汉化包之一。

### 3. **后续更新**

- 由于我可能不再频繁使用 Proteus，后续更新需要大家的支持。
- 如果你需要更新汉化包，请在 [Issue](https://github.com/picdupe/Proteus-Chinese/issues) 中提交请求，并将最新的 `source_en.ts` 文件发给我。
- 我会在一周内完成更新。

---

## 贡献与反馈

欢迎提交 [Issue](https://github.com/picdupe/Proteus-Chinese/issues) 或 [Pull Request](https://github.com/picdupe/Proteus-Chinese/pulls) ，提出建议或改进方案！

---

## 使用指南

### 系统要求
- Proteus 8.0 及以上版本
- Windows 7/8/10/11 操作系统
- 管理员权限（用于文件写入/替换）

### 安装步骤

1. **下载汉化包**
- 从 [Releases](https://github.com/picdupe/Proteus-Chinese/releases) 下载 `qt_zh_CN.qm` 文件。【后续如有更新，请选择与你版本所对应的汉化包】

2. **安装汉化包**
- 将汉化文件复制到 Proteus 安装目录下的 Translations 文件夹。**例如：**：
  ```
  D:\Program Files\Labcenter Electronics\Proteus 9 Demonstration\Translations 
  ```
- 将 `qt_zh_CN.qm` 文件拖入 Translations 文件夹

3. **启用汉化**
   
- 重启 Proteus 即可体验中文界面
   

### 卸载方法

- 删除 `qt_zh_CN.qm` 文件即可

---

## 参与贡献

我们欢迎社区成员参与项目改进！

### 贡献方式
- **翻译校对**：帮助优化现有翻译
- **术语建议**：提出专业术语的准确译法
- **Bug 反馈**：报告翻译错误或界面显示问题
- **文档完善**：改进使用说明和开发文档

### 贡献流程
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 版本记录

### v9.1 SP2 Build 42460
- 初始版本发布
- 完成核心界面汉化
- 建立翻译工作流程
- 实现百度翻译 API 集成

### 未来计划
- [ ] 完整帮助文档汉化
- [ ] 在线术语库系统
- [ ] 自动化翻译更新脚本
- [ ] 社区协作翻译平台

## 致谢

- 感谢百度翻译 API 提供的技术支持
- 感谢所有参与校对和测试的贡献者
- 感谢 Proteus 用户社区的支持与反馈

---

## 许可证
本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- **项目主页**: [GitHub Repository](https://github.com/picdupe/Proteus-Chinese)
- **问题反馈**: [Issues](https://github.com/picdupe/Proteus-Chinese/issues)
- **讨论交流**: [Discussions](https://github.com/picdupe/Proteus-Chinese/discussions)

---

<p align="center">如果这个项目对您有帮助，欢迎 Star 支持！</p>

---

**注意**：汉化包仅适用于 `Proteus 9.1 SP2 Build 42460` 版本，其他版本可能不兼容。

---

## 法律声明与使用须知

### 版权说明
- Proteus 是 Labcenter Electronics Ltd. 的注册商标
- 本项目为独立的第三方汉化项目，与官方无任何关联
- 所有翻译文件仅用于学习和交流目的

### 重要提示
1. **正版要求**
   - 使用本项目需要您已购买并安装正版 Proteus 软件
   - 本项目不提供任何形式的破解、激活或授权绕过工具
   - 请尊重软件开发者的知识产权

2. **使用限制**
   - 本汉化包仅适用于已授权的合法副本
   - 不得将本项目内容用于商业用途
   - 不得将汉化文件与破解软件捆绑发布

3. **责任声明**
   - 本项目仅提供界面汉化，不修改软件核心功能
   - 使用本汉化包造成的任何问题，项目维护者不承担责任
   - 如您未购买正版授权，请立即停止使用本项目

### 获取正版软件
- 官方购买渠道：[Labcenter Electronics](https://www.labcenter.com/)
- 官方授权代理商查询：[全球经销商列表](https://www.labcenter.com/buy/buyagents/)

### 合规使用建议

# 正确使用方式
 - 购买正版 Proteus 软件
 - 安装官方原版程序
 - 应用本汉化语言包
 - 享受中文界面体验

# 禁止行为
 - 使用破解版 Proteus
 - 传播破解补丁或注册机
 - 修改汉化包用于侵权用途

---