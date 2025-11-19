#!/bin/bash
# 批量将 tck 文件转换为 0/1 mask
# 使用 mrtrix3 的 tckmap 工具

# 输入与输出主目录
in_root="/media/UG3/xieyu/fiber_query/HCP/fiber_recognize_results"
ref_root="/media/UG3/xieyu/fiber_query/HCP/T1_un_reg"
out_root="/media/UG3/xieyu/fiber_query/HCP/fiber_recognize_results_mask"

# 遍历所有受试者目录
for subj_dir in "$in_root"/*; do
    subj=$(basename "$subj_dir")
    ref="${ref_root}/${subj}/T1w_acpc_dc_restore_brain.nii.gz"
    fiber_dir="${subj_dir}/reco_bundle_10k_results"
    out_dir="${out_root}/${subj}/reco_bundle_10k_results"

    if [ ! -f "$ref" ]; then
        echo "⚠️ 参考文件不存在: $ref"
        continue
    fi
    if [ ! -d "$fiber_dir" ]; then
        echo "⚠️ 未找到纤维结果目录: $fiber_dir"
        continue
    fi

    mkdir -p "$out_dir"

    echo "▶️ 处理样本: $subj"

    # 遍历该样本下的所有 tck 文件
    for tck_file in "$fiber_dir"/*.tck; do
        [ -e "$tck_file" ] || continue  # 跳过空目录
        bundle_name=$(basename "$tck_file" .tck)
        out_mask="${out_dir}/${bundle_name}.nii.gz"

        if [ -f "$out_mask" ]; then
            continue
        fi

        tmp="${out_dir}/tmp.nii.gz"

        echo "  → 转换: $bundle_name"

        # 使用 mrtrix 的 tckmap 命令生成 0/1 mask
        tckmap "$tck_file" "$tmp" -template "$ref" -force

        # 将非零体素阈值化为1（确保是0/1 mask）
        mrthreshold "$tmp" "$out_mask" -abs 0.1
        rm "$tmp"
    done
done
