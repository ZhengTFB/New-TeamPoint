from datetime import datetime, timedelta
def cl():
    # 读取数据并记录每个人每一天的得分，以及确定日期范围
    data = {}
    start_dt = None
    end_dt = None
    sc=[]
    with open("file.txt", "r", encoding="utf-8") as f:
        for line in f:
            fields = line.strip().split()
            if len(fields) < 4:
                continue
            score, name, date_str, time_str = int(fields[0]), fields[1], fields[3], fields[4]
            try:
                dt = datetime.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H:%M:%S').date()
            except ValueError:
                continue  # 无法识别���日期格式，跳过该行数据
            key = (name, dt)
            if start_dt is None or dt < start_dt:
                start_dt = dt
            if end_dt is None or dt > end_dt:
                end_dt = dt
            if key not in data:
                data[key] = 0
            data[key] += score

    # 构造日期序列和人名序列
    dates = [start_dt + timedelta(days=num) for num in range((end_dt - start_dt).days + 1)]
    names = sorted(set(key[0] for key in data))

    # 输出每个人每一天的得分
    output_data = {}
    for date in dates:
        output_data[str(date)] = {}   # 每个日期对应的字典
        for name in names:
            key = (name, date)
            score = data.get(key, 0)
            output_data[str(date)][name] = score

    # 按照每个人每一天的得分输出统计结果
    for name in names:
        scores = []
        for date in dates:
            score = output_data[str(date)].get(name, 0)
            scores.append(score)
        total_score = 0
        res=[]
        for slr in scores:
          total_score += slr
          res.append(total_score)
        sc.append([name] + res)
    return sc
