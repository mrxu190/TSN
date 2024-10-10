import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from numpy.distutils.misc_util import yellow_text, red_text

# x坐标范围
flows = np.array([20, 25, 30, 35, 40, 45, 50, 55])

SPR = ([6.15, 8.17, 10.45, 12.42, 14.75, 16.70, 19.05, 20.94],[6.45, 7.63, 9.43, 11.58, 13.63, 15.56, 17.34, 19.47],[5.68, 7.38, 8.90, 11.28, 12.98, 15.11, 16.63, 18.25])

LB_KPR = ([5.13, 6.73, 8.24, 10.01, 11.49, 13.23, 14.82, 16.47],[4.87, 6.34, 7.89, 9.46, 10.98, 12.59, 14.09, 15.64],[4.63, 6.04, 7.54, 8.98, 10.47, 11.91, 13.47, 14.89])

rand = ([5.49, 7.07, 8.46, 10.04, 11.60, 13.32, 15.10, 16.57], [5.20, 6.53, 8.25, 9.51, 11.28, 12.76, 14.27, 15.85], [4.96, 6.62, 7.63, 9.22, 10.97, 12.21, 13.54, 15.42])

KSP = ([5.50, 7.18, 8.74, 11.03, 12.15, 13.83, 15.65, 17.39],[5.17, 6.69, 8.26, 9.91, 11.39, 13.21, 14.66, 16.26],[4.87, 6.36, 7.80, 9.29, 10.86, 12.26, 13.78, 15.30])

LB_DRR = ([5.57, 7.18, 8.85, 10.64, 12.15, 13.87, 15.60, 17.3,],[5.44, 6.69, 8.26, 9.80, 11.39, 13.14, 14.92, 16.23],[5.11, 6.36, 7.79, 9.29, 10.74, 12.25, 13.79, 15.30])

# Create subplots
fig, axs = plt.subplots(1, 3, figsize=(12, 4))

#     ax.plot(flows, schedulability_tabu, '-s', label='KSP')  flows为x轴数据，schedulability_tabu为y轴数据
# Plot schedulability on different topologies
for i, ax in enumerate(axs):
    ax.plot(flows, SPR[i], '-o', label='SPR')
    ax.plot(flows, KSP[i], '-s', label='KSP')
    ax.plot(flows, rand[i], '-d', label='RAND')
    ax.plot(flows, LB_DRR[i], '-^', label='LB_DRR', color='pink')
    ax.plot(flows, LB_KPR[i], '-p', label='LB_KPR', color='red')
    ax.set_xlabel('#  Flow Num')
    ax.set_ylabel('Load Performance')
    ax.set_ylim(0, 25)
    ax.set_xticks(flows)   #显示刻度由flows决定
    ax.grid(True)
    ax.legend()
    # 选择放大区域的坐标
    x1, x2, y1, y2 = 37.5, 42.5, 8, 15

    # 在原坐标系中绘制矩形框
    rect = plt.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2, edgecolor='red', facecolor='none', linestyle='--')
    ax.add_patch(rect)

    # 创建插入坐标轴


    ax_inset = inset_axes(ax, width="20%", height="20%",loc='lower right')
    pos = ax_inset.get_position()
    # 例如，调整位置（x0, y0, width, height）
    new_position = [pos.x0 + 0.05, pos.y0 + 0.05, pos.width, pos.height]  # 向右和向上移动
    ax_inset.set_position(new_position)


    ax_inset.plot(flows, SPR[i], '-o', label='SPR')
    ax_inset.plot(flows, KSP[i], '-s', label='KSP')
    ax_inset.plot(flows, rand[i], '-d', label='RAND')
    ax_inset.plot(flows, LB_DRR[i], '-^', label='LB_DRR',color='pink')
    ax_inset.plot(flows, LB_KPR[i], '-p', label='LB_KPR',color='red')
    ax_inset.set_xlim(39.5, 40.5)  # 放大区域
    ax_inset.set_ylim(10.5, 12)  # 放大区域
    ax_inset.grid(True)

    # 隐藏插入图的坐标轴和边框
    ax_inset.axis('off')

    # 显示插入图的边框
    mark_inset(ax, ax_inset, loc1=2, loc2=4, fc="none")

    # # 选择放大区域的坐标
    # x1, x2, y1, y2 = 30, 50, 10, 20
    #
    # # 在原坐标系中绘制矩形框
    # rect = plt.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=1, edgecolor='red', facecolor='none', linestyle='--')
    # ax.add_patch(rect)
    # ax_inset = inset_axes(ax, width="30%", height="30%", loc='lower right')
    # ax_inset.plot(flows, SPR[i], '-o', label='SPR')
    # ax_inset.plot(flows, KSP[i], '-s', label='KSP')
    # # ax_inset.set_xlim(30, 50)  # Set limits for zoomed area
    # # ax_inset.set_ylim(9, 10)
    # ax_inset.grid(True)








# Plot average run time on different topologies
# for i, ax in enumerate(axs[1]):
#     ax.plot(flows, runtime_ours, '-o', label='Ours')
#     ax.plot(flows, runtime_tabu, '-s', label='Tabu')
#     ax.plot(flows, runtime_dsk, '-^', label='DSK')
#     ax.plot(flows, runtime_genetic, '-d', label='Genetic')
#     ax.plot(flows, runtime_random, '-p', label='Random')
#     ax.plot(flows, runtime_ilp, '-x', label='ILP')
#     ax.set_xlabel('# of flows')
#     ax.set_ylabel('Average run time(s)')
#     ax.set_yscale('log')  # Logarithmic scale for time
#     ax.grid(True)
#     ax.legend()

plt.tight_layout()
plt.show()