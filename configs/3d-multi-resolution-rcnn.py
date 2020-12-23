# model settings
model = dict(
    type='MaskRCNN3D2Scales',
    backbone=dict(
        type='ResNet3D',
        depth=50,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        frozen_stages=-1,
        style='pytorch'),
    neck=dict(
        type='FPN3D',
        in_channels=[64, 128, 256, 512],
        out_channels=64,
        num_outs=5),
    rpn_head=dict(
        type='RPNHead3D',
        in_channels=64,
        feat_channels=64,
        anchor_scales=[2],
        anchor_depth_scales=[2],
        anchor_ratios=[1.0],
        anchor_strides=[4, 8, 16, 32, 64],
        anchor_strides_depth=[2, 4, 8, 16, 32],
        target_means=[.0, .0, .0, .0, .0, .0],
        target_stds=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        use_sigmoid_cls=True),
    rpn_head_2=dict(
        type='RPNHead3D',
        in_channels=64,
        feat_channels=64,
        anchor_scales=[3],
        anchor_depth_scales=[3],
        anchor_ratios=[1.0],
        anchor_strides=[4, 8, 16, 32, 64],
        anchor_strides_depth=[2, 4, 8, 16, 32],
        target_means=[.0, .0, .0, .0, .0, .0],
        target_stds=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        use_sigmoid_cls=True),
    bbox_roi_extractor=dict(
        type='SingleRoIExtractor',
        roi_layer=dict(type='RoIAlign3D', out_size=7, out_size_depth=3, sample_num=2),
        out_channels=64,
        featmap_strides=[4, 8, 16, 32],
        featmap_strides_depth=[2, 4, 8, 16]),
    bbox_head=dict(
        type='SharedFCBBoxHead3D',
        num_fcs=2,
        in_channels=64,
        fc_out_channels=1024,
        roi_feat_size=7,
        roi_feat_size_depth=3,
        num_classes=2,
        target_means=[0., 0., 0., 0., 0., 0.],
        target_stds=[0.1, 0.1, 0.2, 0.2, 0.1, 0.1],
        reg_class_agnostic=False),
    refinement_head=dict(
        type='SharedFCBBoxHead3DRefinement',
        num_fcs=2,
        in_channels=64,
        fc_out_channels=1024,
        roi_feat_size=7,
        roi_feat_size_depth=3,
        num_classes=2,
        target_means=[0., 0., 0., 0., 0., 0.],
        target_stds=[0.1, 0.1, 0.2, 0.2, 0.1, 0.1],
        reg_class_agnostic=False),
    mask_roi_extractor=dict(
        type='SingleRoIExtractor',
        roi_layer=dict(type='RoIAlign3D', out_size=14, out_size_depth=10, sample_num=2),
        out_channels=64,
        featmap_strides=[4, 8, 16, 32],
        featmap_strides_depth=[2, 4, 8, 16]),
    mask_head=dict(
        type='FCNMaskHead3D',
        num_convs=4,
        in_channels=64,
        conv_out_channels=64,
        num_classes=2),
    refinement_mask_head=dict(
        type='FCNMaskHead3D',
        num_convs=4,
        in_channels=64,
        conv_out_channels=64,
        num_classes=2))
# model training and testing settings
train_cfg = dict(
    rpn=dict(
        assigner=dict(
            type='MaxIoUAssigner',
            pos_iou_thr=0.7,
            neg_iou_thr=0.3,
            min_pos_iou=0.3,
            ignore_iof_thr=-1),
        sampler=dict(
            type='RandomSampler',
            num=256,
            pos_fraction=0.5,
            neg_pos_ub=-1,
            add_gt_as_proposals=False),
        allowed_border=0,
        pos_weight=3,
        smoothl1_beta=1 / 9.0,
        debug=False),
    rpn_proposal=dict(
        nms_across_levels=False,
        nms_pre=2000,
        nms_post=2000,
        max_num=2000,
        nms_thr=0.7,
        min_bbox_size=0),
    rcnn=dict(
        assigner=dict(
            type='MaxIoUAssigner',
            pos_iou_thr=0.5,
            neg_iou_thr=0.5,
            min_pos_iou=0.5,
            ignore_iof_thr=-1),
        sampler=dict(
            type='RandomSampler',
            num=512,
            pos_fraction=0.25,
            neg_pos_ub=-1,
            add_gt_as_proposals=True),
        mask_size=28,
        mask_size_depth=20,
        pos_weight=3,
        debug=False))
dataset_type = 'Coco3D2ScalesDataset'
# dataset settings
test_cfg = dict(
    rpn=dict(
        nms_across_levels=False,
        nms_pre=2000,
        nms_post=2000,
        max_num=2000,
        nms_thr=0.7,
        min_bbox_size=0),
    rcnn=dict(
        score_thr=0.2,
        nms=dict(type='nms', iou_thr=0.5),
        max_per_img=2000,
        mask_thr_binary=0.25))
data_root = 'data/Stroke_v4/COCO-full-vol/'
data_root_2 = 'data/Stroke_v4-14TB/COCO-full-vol-1dot5x/'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
data2_2scales = dict(
    imgs_per_gpu=1,
    workers_per_gpu=4,
    train=dict(
        type=dataset_type,
        ann_file=data_root_2 + 'annotations/instances_train2019_full.json',
        img_prefix=data_root_2 + 'train/COCO_train_full2019',
        img_scale=(768, 768), #1.5
        img_norm_cfg=img_norm_cfg,
        size_divisor=32,
        flip_ratio=0,
        with_mask=True,
        with_crowd=False,
        with_label=True,
        extra_aug=dict(
            random_crop_3d=dict(
                min_ious=(0.1, 0.3, 0.5, 0.7, 0.9)))),
    val=dict(
        type=dataset_type,
        ann_file=data_root_2 + 'annotations/instances_valid2019_full.json',
        img_prefix=data_root_2 + 'valid/COCO_valid_full2019',
        img_scale=(768, 768),
        img_norm_cfg=img_norm_cfg,
        size_divisor=32,
        flip_ratio=0,
        with_mask=False,
        with_crowd=False,
        with_label=True,
        ann_file_volume=data_root_2 + 'annotations/instances_valid2019_full.json'),
    test=dict(
        type=dataset_type,
        ann_file=data_root_2 + 'annotations/instances_test2019_full.json',
        img_prefix=data_root_2 + 'test/COCO_test_full2019',
        img_scale=(768, 768),
        img_norm_cfg=img_norm_cfg,
        size_divisor=32,
        flip_ratio=0,
        with_mask=True,
        with_label=False,
        test_mode=True,
        ann_file_volume=data_root_2 + 'annotations/instances_test2019_full.json'))
data = dict(
    imgs_per_gpu=1,
    workers_per_gpu=4,
    train=dict(
        type=dataset_type,
        ann_file=data_root + 'annotations/instances_train2019_full.json',
        img_prefix=data_root + 'train/COCO_train_full2019',
        img_scale=(512, 512),
        img_norm_cfg=img_norm_cfg,
        size_divisor=32,
        flip_ratio=0,
        with_mask=True,
        with_crowd=False,
        with_label=True,
        data2=data2_2scales['train'],
        extra_aug=dict(
            random_crop_3d=dict(
                min_ious=(0.1, 0.3, 0.5, 0.7, 0.9)))),
    val=dict(
        type=dataset_type,
        ann_file=data_root + 'annotations/instances_valid2019_full.json',
        img_prefix=data_root + 'valid/COCO_valid_full2019',
        img_scale=(512, 512),
        img_norm_cfg=img_norm_cfg,
        size_divisor=32,
        flip_ratio=0,
        with_mask=False,
        with_crowd=False,
        with_label=True,
        ann_file_volume=data_root + 'annotations/instances_valid2019_full.json',
        data2=data2_2scales['val']),
    test=dict(
        type=dataset_type,
        ann_file=data_root + 'annotations/instances_test2019_full.json',
        img_prefix=data_root + 'test/COCO_test_full2019',
        img_scale=(512, 512),
        img_norm_cfg=img_norm_cfg,
        size_divisor=32,
        flip_ratio=0,
        with_mask=True,
        with_label=False,
        test_mode=True,
        ann_file_volume=data_root + 'annotations/instances_test2019_full.json',
        data2=data2_2scales['test']))
# optimizer
optimizer = dict(type='SGD', lr=0.001, momentum=0.9, weight_decay=0.0001)
optimizer_config = dict(grad_clip=dict(max_norm=35, norm_type=2))
# learning policy
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=10,
    warmup_ratio=1.0 / 3,
    # step=[8, 11])
    step=[2500, 3000])
checkpoint_config = dict(interval=5)
# yapf:disable
log_config = dict(
    interval=1,
    hooks=[
        dict(type='TextLoggerHook'),
        # dict(type='TensorboardLoggerHook')
    ])
# yapf:enable
# runtime settings
total_epochs = 2000
dist_params = dict(backend='nccl')
log_level = 'INFO'
work_dir = './work_dirs/checkpoints/3d-multi-resolution-rcnn'
load_from = None
resume_from = None
workflow = [('train', 1)]
interval = 5