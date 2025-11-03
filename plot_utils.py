import matplotlib.pyplot as plt

def plot_cumulative_returns(results_dict, title="策略累计收益比较", save_path=None):
    """
    绘制多个策略的累计收益曲线（仅保存不展示）
    参数：
        results_dict: dict，格式为 {'策略名': DataFrame}，DataFrame需包含 'cumulative_return' 列
        title: 图标题
        save_path: 图像保存路径（建议以 .png 结尾）
    """
    plt.figure(figsize=(10, 6))
    for name, df in results_dict.items():
        plt.plot(df['cumulative_return'].values, label=name)
    plt.title(title)
    plt.xlabel("时间步")
    plt.ylabel("累计收益（净值）")
    plt.legend()
    plt.grid(True)
    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"图像已保存：{save_path}")
    plt.close()  # 只保存，不显示
