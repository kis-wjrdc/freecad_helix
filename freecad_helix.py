import FreeCAD as App
import Part

# ドキュメントを取得または作成
doc = App.ActiveDocument
if doc is None:
    doc = App.newDocument()

# パラメトリックな設定
radius_helix = 10  # ヘリックスの半径
section_angle = 30  # 各セクションの回転角度（度）
pitches = [1, 2, 3, 4]  # ピッチリスト
normal_pitch = 5  # 通常のピッチ
reverse_direction = True  # 逆回転を選択するためのパラメータ（Trueにすると逆回転）
angle_offset = section_angle * len(pitches) * 2  # 通常ピッチ区間の角度オフセット
normal_turns = 4 - (angle_offset / 360)  # 通常ピッチの正確な回転数

# ピッチが1から4まで増加
combined_pitches = pitches.copy()

# 通常ピッチ区間
combined_pitches.append(normal_pitch)

# ピッチが4から1まで減少
combined_pitches += pitches[::-1]

# 各セクションの高さを計算
heights = [(section_angle / 360) * pitch for pitch in pitches]
heights.append(normal_pitch * normal_turns)  # 通常ピッチ区間の高さ
heights += [(section_angle / 360) * pitch for pitch in pitches[::-1]]

# 回転方向の設定
rotation_direction = 1 if not reverse_direction else -1

# 最初のセクションを作成
combined_helix = Part.makeHelix(combined_pitches[0], heights[0], radius_helix, 0, reverse_direction)

# 連続した螺旋を作成
z_offset = heights[0]
angle_accum = section_angle * rotation_direction

for i in range(1, len(combined_pitches)):
    helix = Part.makeHelix(combined_pitches[i], heights[i], radius_helix, 0, reverse_direction)
    placement = App.Placement(App.Vector(0, 0, z_offset), App.Rotation(App.Vector(0, 0, 1), angle_accum))
    helix.Placement = placement

    # オフセットと角度を更新
    z_offset += heights[i]

    if i < len(pitches):  # 開始区間
        angle_accum += section_angle * rotation_direction
    elif i == len(pitches):  # 通常ピッチ区間
        angle_accum += 360 * normal_turns * rotation_direction
    else:  # 終了区間
        angle_accum += section_angle * rotation_direction

    # 螺旋を結合
    combined_helix = combined_helix.fuse(helix)

# 螺旋を表示
Part.show(combined_helix)

# ドキュメントを更新
doc.recompute()
