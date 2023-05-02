# ☄️New-TeamPoint
更全面、更方便、更优雅
## 新一代积分程序
New-TeamPoint
### 0.总体介绍
- 创作日期：2023/5/2--[正钛汾钸](https://github.com/zhengtfb)
- 支持[记录个人积分](#jump_1)
- 支持[自定义成员名单](#jump_2)
- 支持[生成前三名和警示栏](#jump_3)
- 支持[自动分析并生成每个人积分变化的折线图](#jump_4)
### 1.记录个人积分
<a id="jump_1"></a>
![积分界面](https://github.com/zhengtfb/New-TeamPoint/blob/main/%E4%B8%BB%E7%95%8C%E9%9D%A2.JPG)
- 可选择积分类型，简洁明了
- 下拉式列表选择被积分人，免除了打字的烦恼，方便快捷
- 可选填积分原因，方便日后核实
### 2.自定义成员名单
<a id="jump_2"></a>
```json
{
    "author": "正钛汾钸",
    "lunch_break_personnel": ["人员1", "人员2","人员..."],
    "creation_date":"2023.5.1",
    "statistics_key":"1234",
    "jingshi":"0"
}
```
lunch_break_personnel栏，控制被计分人员，且在下来列表中显示，方便快捷
### 3.生成前三名和警示栏
<a id="jump_3"></a>
- 自动计算每个人累计积分，分析前三名，并显示在界面下方
- 根据json文件jingshi栏，生成总分低于该分数的人，显示在界面下方，予以警告
### 4.自动分析并生成每个人积分变化的折线图
<a id="jump_4"></a>
- 通过cl函数，计算每人每天得分
- 自动识别不支持的时间格式，防止程序阻塞
```python
try:
  dt = datetime.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H:%M:%S').date()
except ValueError:
  continue  # 无法识别���日期格式，跳过该行数据
```
- 通过matplotlib.pyplot库生成折线图，快捷简便
- 自动合成长图，方便查阅
- 设置统计密码（json文件statistics_key栏），保护数据安全
