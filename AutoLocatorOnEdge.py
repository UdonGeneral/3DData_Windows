def _create_locator_for_joint(
    self,
    joint,
    use_translate,
    use_rotate,
    use_scale
):
    """固定用と手動調整用のロケータを作成する。"""

    joint_short_name = joint.split("|")[-1]
    safe_name = joint_short_name.replace(":", "_")

    # 固定用ロケータ
    lock_locator = cmds.spaceLocator(
        name="{}_LOCK_LOC".format(safe_name)
    )[0]

    # 手動調整用ロケータ
    adjust_locator = cmds.spaceLocator(
        name="{}_ADJUST_LOC".format(safe_name)
    )[0]

    # ジョイントのワールド行列
    joint_world_matrix = cmds.xform(
        joint,
        query=True,
        worldSpace=True,
        matrix=True
    )

    # 固定用ロケータをジョイントに一致
    cmds.xform(
        lock_locator,
        worldSpace=True,
        matrix=joint_world_matrix
    )

    # 調整用ロケータもジョイントに一致
    cmds.xform(
        adjust_locator,
        worldSpace=True,
        matrix=joint_world_matrix
    )

    # 調整用ロケータを固定用ロケータの子にする
    cmds.parent(adjust_locator, lock_locator)

    # 親子化した後、ローカルトランスフォームをゼロにする
    cmds.setAttr(adjust_locator + ".translate", 0, 0, 0)
    cmds.setAttr(adjust_locator + ".rotate", 0, 0, 0)
    cmds.setAttr(adjust_locator + ".scale", 1, 1, 1)

    # 調整用ロケータからジョイントを制御
    if use_translate and use_rotate:
        cmds.parentConstraint(
            adjust_locator,
            joint,
            maintainOffset=False,
            name="{}_LOCK_parentConstraint".format(safe_name)
        )
    else:
        if use_translate:
            cmds.pointConstraint(
                adjust_locator,
                joint,
                maintainOffset=False,
                name="{}_LOCK_pointConstraint".format(safe_name)
            )

        if use_rotate:
            cmds.orientConstraint(
                adjust_locator,
                joint,
                maintainOffset=False,
                name="{}_LOCK_orientConstraint".format(safe_name)
            )

    if use_scale:
        cmds.scaleConstraint(
            adjust_locator,
            joint,
            maintainOffset=False,
            name="{}_LOCK_scaleConstraint".format(safe_name)
        )

    return adjust_locator