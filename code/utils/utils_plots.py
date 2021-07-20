import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import math

import seaborn as sns
import collections

mpl.use('TkAgg')
sns.set()


LOC_DICT = {2: 'upper left',
            6: 'center left',
            3: 'lower left',
            9: 'upper center',
            8: 'lower center',
            1: 'upper right',
            7: 'center right',
            4: 'lower right'}


def multibar(data, set1, orientation, x, y, hue=None, col=None, row=None, order=None, height=4, aspect=1.5, rotation=0,
             space_x=None, space_y=None,
             show_values=False,
             legend_out=False, legend=True, legend_loc=None, legend_ncol=1, legend_borderaxespad=0, legend_mode=None,
             # legend_size=(0.5, 0.5),
             sharex=True, sharey=True,
             kind="bar",
             ha=None, va=None, zero_axis=False,
             rc=None,
             xticks=None, xticklabels=None, xstep=None,
             yticks=None, yticklabels=None, ystep=None, ysteptype="absolute",
             **kwargs):
    # normal orientation="h"
    fig, x, y, col, row, rotation, space_x, space_y = init(set1, orientation, x, y, col, row,
                                                           space_x, space_y, rotation, rc)
    legend_out_plot = False if legend_loc is not None else legend_out
    legend_plot = False if legend_loc is not None else legend

    plot = sns.catplot(data=data, x=x, y=y,
                       hue=hue, hue_order=np.unique(data[hue]), row=row, col=col,
                       order=order,
                       kind=kind,
                       height=height, aspect=aspect,
                       sharex=sharex,
                       sharey=sharey,
                       orient=orientation,
                       legend_out=legend_out_plot,
                       legend=legend_plot,
                       **kwargs)
    if xstep is not None:
        plot.set_xticklabels(step=xstep)
    else:
        if xticks is not None:
            plot.set_xticks(xticks)
        if xticklabels is not None:
            plot.set_xticklabels(xticklabels)
    if ystep is not None:
        axes = plot.axes
        shape = axes.shape
        for i in range(0, shape[0]):
            if sharey:
                ylim = axes[i, 0].get_ylim()
                yticks, yticklabels = _get_yticks(ylim, yticks, yticklabels, ystep, ysteptype)
                axes[i, 0].set(yticks=yticks)
                axes[i, 0].set(yticklabels=yticklabels)
            else:
                for j in range(0, shape[1]):
                    ylim = axes[i, j].get_ylim()
                    yticks, yticklabels = _get_yticks(ylim, yticks, yticklabels, ystep, ysteptype)
                    axes[i, j].set(yticks=yticks)
                    axes[i, j].set(yticklabels=yticklabels)

    if yticks is not None:
        plot.set(yticks=yticks)
    if yticklabels is not None:
        plot.set(yticklabels=yticklabels)

    plot.set_xticklabels(rotation=rotation)
    axes = plot.axes
    if show_values:
        axes = show_values_on_bars(axes, h_v=orientation, space_x=space_x, space_y=space_y, rotation=rotation,
                                   ha=ha, va=va, zero_axis=zero_axis)
        plot.axes = axes

    if legend_loc is not None:
        if legend_out:
            ax, bbox, lloc = _get_legend_param(axes, legend_loc, legend_mode)
            # if legend_mode == "expand":
            #     bbox = (bbox[0], bbox[1], legend_size[0], legend_size[1])

            ax.legend(loc=lloc, ncol=legend_ncol, bbox_to_anchor=bbox, borderaxespad=legend_borderaxespad,
                      mode=legend_mode)

    fig = plot.fig
    return fig, plot, axes


def bar(title=None, set1=None, show_values=False, **kwargs):
    fig = init(set1)
    plot = sns.barplot(**kwargs).set_title(title)
    fig = plot.get_figure()
    axes = plot.axes
    if show_values:
        axes = show_values_on_bars(axes, h_v="v", space_x=0, space_y=0.5, rotation=90)

    # if set is not None:
    #     fig, plot, axes = setup(fig, plot, axes, set)
    return fig, plot, axes


def init(set=None, orientation="h", x=None, y=None, col=None, row=None, space_x=None, space_y=None, rotation=0,
         rc=None):
    if set == "paper":
        rc = {"font.size": 12,
              "axes.titlesize": 20,
              "axes.labelsize": 18,
              "xtick.labelsize": 14,
              "ytick.labelsize": 14,
              "legend.fontsize": 14,
              "legend.title_fontsize": 16,
              } if rc is None else rc
        sns.set_style("whitegrid")
        sns.set_context("paper", rc=rc)
        # sns.set_palette("Reds")
        fig = plt.figure(figsize=(10, 6))

    elif set == "paper, multicolumn":
        fig = None
        sns.set_style("whitegrid")
        rc = {"font.size": 12,
              "axes.titlesize": 16,
              "axes.labelsize": 14,
              "xtick.labelsize": 12,
              "ytick.labelsize": 12,
              "legend.fontsize": 14,
              "legend.title_fontsize": 14,
              } if rc is None else rc

        sns.set_context("paper", rc=rc)
        if orientation == "v":
            x = x
            y = y
            row = row
            col = col
            rotation = 90
            space_x = 0 if space_x is None else space_x
            space_y = -5 if space_y is None else space_y
        elif orientation == "h":
            x = y
            y = x
            row = col
            col = row
            rotation = 0
            space_x = 0 if space_x is None else space_x
            space_y = 0 if space_y is None else space_y
        else:
            raise TypeError
    else:
        fig = plt.figure(figsize=(10, 6))
    return fig, x, y, col, row, rotation, space_x, space_y


def show_values_on_bars(axes, h_v="v", space_x=0.4, space_y=0.4, rotation=0, ha=None, va=None, zero_axis=False):
    def _show_on_single_plot(ax, ha=None, va=None):
        if h_v == "v":
            ha = "center" if ha is None else ha
            va = "center" if va is None else va
            for p in ax.patches:
                _x = p.get_x() + p.get_width() / 2 + float(space_x)
                _y = p.get_y() + p.get_height() + float(space_y)
                value = 0 if (np.isnan(p.get_height())) else round(p.get_height(), 1)
                txt = ax.text(_x, _y, value, ha=ha, va=va, rotation=rotation)
                if zero_axis:
                    ax.figure.canvas.draw()
                    bb = txt.get_window_extent()
                    co = ax.transAxes.inverted().transform(bb)
                    if co[0][1] < 0:
                        # (_, _y_add) = ax.transData.transform_point((co[0][0], co[0][1]))
                        # (_, _y_add) = ax.transData.transform_point((0, 0))*abs(co[0][1])
                        (_, _y_add) = ax.transLimits.inverted().transform(
                            ax.transData.transform_point(co[0]) - ax.transData.transform_point((0, 0)))

                        txt.set_y(_y + abs(_y_add))

        elif h_v == "h":
            ha = "left" if ha is None else ha
            va = "center" if va is None else va
            for p in ax.patches:
                _x = p.get_x() + p.get_width() + float(space_x)
                _y = p.get_y() + p.get_height() + float(space_y)
                value = 0 if (np.isnan(p.get_width())) else round(p.get_width(), 1)
                txt = ax.text(_x, _y, value, ha=ha, va=va, rotation=rotation)

    if isinstance(axes, np.ndarray):
        for idx, ax in np.ndenumerate(axes):
            _show_on_single_plot(ax, ha, va)
    else:
        _show_on_single_plot(axes, ha, va)
    return axes


def confusion_matrix(data,
                     title,
                     map_act=None,
                     map_pred=None,
                     type_plt="raw",
                     font_scale=1,
                     cmap="Blues",
                     rc=None,
                     figsize=(5.5, 4.5),
                     cbar=False,
                     yticks_rotation=0,
                     xticks_rotation=30,
                     title_x_pos=0,
                     axes_labelpad=4):

    sns.set_style("whitegrid")
    rc = {"font.size": 14,
          "axes.titlesize": 18,
          "axes.labelsize": 16,
          "xtick.labelsize": 14,
          "ytick.labelsize": 14,
          "legend.fontsize": 14,
          "legend.title_fontsize": 16,
          } if rc is "auto" else rc

    sns.set_context("paper", font_scale=font_scale, rc=rc)

    if type_plt == "raw":
        df = pd.DataFrame(data=np.column_stack((data['y_actual'], data['y_pred_total'])), columns=[
            'y_actual', 'y_pred_total'])

        var_act = map_act.values()
        var_pred = map_pred.values()

        df['y_actual'] = df['y_actual'].map(map_act)
        df['y_pred_total'] = df['y_pred_total'].map(map_pred)
        confusion_matrix_ = pd.crosstab(df['y_actual'].replace(np.nan, 'NaN'), df['y_pred_total'].replace(np.nan, 'NaN'),
                                        rownames=['Actual label'],
                                        colnames=['Predicted label'],
                                        normalize="index", dropna=False)

        confusion_matrix_ = confusion_matrix_.reindex(index=var_act, columns=var_pred, fill_value=0)
    elif type_plt == "cm":
        confusion_matrix_ = data
        df = data
    else:
        raise NameError("type should be 'cm' or 'raw'")

    fig = plt.figure(figsize=figsize)
    plot = sns.heatmap(confusion_matrix_, annot=True, cmap=cmap, fmt='.1%', cbar=cbar)

    for item in plot.get_xticklabels():
        item.set_rotation(xticks_rotation)
    for item in plot.get_yticklabels():
        item.set_rotation(yticks_rotation)

    ax = plot.axes
    ax.xaxis.labelpad = axes_labelpad
    ax.yaxis.labelpad = axes_labelpad

    plt.title(title, loc='left', x=title_x_pos)
    # plt.show()

    return fig, df, confusion_matrix_


def get_data_plt(df, index_columns):
    """
    results is a dataframe
    :param df: dataframe as input
    :type df: pd.DataFrame
    :param index_columns: columns which should be index
    :type index_columns: list
    :return:
    """
    data = collections.OrderedDict()

    if len(index_columns) == 1:
        result = df.set_index(index_columns[0]).stack().reset_index()
        result = result.rename(columns={'level_1': 'description', 0: 'value'})
        data[""] = result
    elif len(index_columns) > 1:
        unique_elements = df[index_columns[0]].unique()
        for element in unique_elements:
            result = df.loc[df[index_columns[0]] == element].set_index(index_columns).stack().reset_index()
            result = result.drop(columns=index_columns[0])
            column = [x for x in result.columns if "level" in str(x)]
            result = result.rename(columns={column[0]: 'description', 0: 'value'})
            data[element] = result.copy(deep=True)

    else:
        raise ValueError

    return data


def _get_yticks(ylim, yticks=None, yticklabels=None, ystep=None, ysteptype="absolute"):
    if ysteptype == "absolute":
        yticks = list(np.arange(ylim[0], ylim[1], ystep))
        yticklabels = yticks
    elif ysteptype == "percentage":
        yticks = list(np.arange(ylim[0], ylim[1], ystep * (ylim[1] - ylim[0])))
        yticklabels = yticks
    return yticks, yticklabels


def _get_bbox_to_anchor(loc, mode=None):
    # from https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
    if type(loc) == int:
        loc = LOC_DICT[loc]

    if loc == 'upper left':
        bbox = (-0.05, 1)
        lloc = 'upper right'
    elif loc == 'center left':
        bbox = (-0.05, 0.5)
        lloc = 'center right'
    elif loc == 'lower left':
        bbox = (-0.05, 0)
        lloc = 'lower right'
    elif loc == 'upper center':
        bbox = (0.5, 1.05) if mode is None else (0, 1.05, 1, 1)
        lloc = 'lower center' if mode is None else 'lower left'
    elif loc == 'lower center':
        bbox = (0.5, -0.05) if mode is None else (0, -0.05, 1, 1)
        lloc = 'upper center' if mode is None else 'upper left'
    elif loc == 'upper right':
        bbox = (1.05, 1)
        lloc = 'upper left'
    elif loc == 'center right':
        bbox = (1.05, 0.5)
        lloc = 'center left'
    elif loc == 'lower right':
        bbox = (1.05, 0)
        lloc = 'lower left'
    else:
        raise NameError("loc has not a useful value")
    return bbox, lloc


def _get_legend_param(axes, loc, mode=None):
    if type(loc) == int:
        loc = LOC_DICT[loc]

    shape = axes.shape

    loc_split = loc.split(" ")
    bbox, lloc = _get_bbox_to_anchor(loc, mode)
    bbox = list(bbox)
    dim = [0, 0]

    if loc_split[0] == "upper":
        dim[0] = 0
    elif loc_split[0] == "center":
        dim[0] = math.floor(shape[0] / 2)
    elif loc_split[0] == "lower":
        dim[0] = shape[0] - 1

    if not(shape[0] % 2) and loc_split[0] == "center":
        bbox[1] = bbox[1] - 0.5

    if loc_split[1] == "left":
        dim[1] = 0
    elif loc_split[1] == "center":
        dim[1] = math.floor(shape[1] / 2)
    elif loc_split[1] == "right":
        dim[1] = shape[1] - 1

    if not(shape[1] % 2) and loc_split[1] == "center":
        bbox[0] = bbox[0] + 0.5

    ax = axes[dim[0], dim[1]]

    # pos = ax.get_xaxis()



    # mpl.use('TkAgg')
    # fig1 = ax.get_figure()
    # ax.remove()
    # fig2 = plt.figure()
    # ax.figure = fig2
    # fig2.axes.append(ax)
    # fig2.add_axes(ax)
    # dummy = fig2.add_subplot(111)
    # ax.set_position(dummy.get_position())
    # dummy.remove()
    # plt.close(fig1)
    # plt.show()

    return ax, bbox, lloc
