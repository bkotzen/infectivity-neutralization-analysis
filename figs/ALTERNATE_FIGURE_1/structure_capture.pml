fetch 7bnn
remove solvent
remove not polymer.protein
set specular, 0
set depth_cue, 0
set ambient, 0.5
set ray_trace_gain, 0
set ray_trace_mode, 1
set ray_trace_color, black
set ray_trace_depth_factor, 1
set ray_trace_disco_factor, 1
set light_count, 2
set ray_opaque_background, 0
show cartoon, chain B
 set cartoon_loop_radius, 0.4
show as spheres, chain A or chain C
show surface, chain A or chain C
hide cartoon, chain A or chain C
set transparency, 0.1
color gray40, chain C
color gray60, chain A
color gray80, chain B
set_color count_Δ19, [0.4588235294117647, 0.4392156862745098, 0.7019607843137254]
color count_Δ19, chain B and (resi 19)
set_color count_T478Q, [0.10588235294117647, 0.6196078431372549, 0.4666666666666667]
color count_T478Q, chain B and (resi 478)
set_color count_D1139Y, [0.8509803921568627, 0.37254901960784315, 0.00784313725490196]
color count_D1139Y, chain B and (resi 1139)
set_color count_S155R, [0.4588235294117647, 0.4392156862745098, 0.7019607843137254]
color count_S155R, chain B and (resi 155)
set_color count_E156G, [0.4588235294117647, 0.4392156862745098, 0.7019607843137254]
color count_E156G, chain B and (resi 156)
set_color count_P1112Q, [0.8509803921568627, 0.37254901960784315, 0.00784313725490196]
color count_P1112Q, chain B and (resi 1112)
set_color count_W152C, [0.4588235294117647, 0.4392156862745098, 0.7019607843137254]
color count_W152C, chain B and (resi 152)
set_color count_Δ145, [0.4588235294117647, 0.4392156862745098, 0.7019607843137254]
color count_Δ145, chain B and (resi 145)
set_color count_Δ142, [0.4588235294117647, 0.4392156862745098, 0.7019607843137254]
color count_Δ142, chain B and (resi 142)
set_color count_N658S, [0.8509803921568627, 0.37254901960784315, 0.00784313725490196]
color count_N658S, chain B and (resi 658)
set_color count_A222V, [0.4588235294117647, 0.4392156862745098, 0.7019607843137254]
color count_A222V, chain B and (resi 222)
set_color count_Δ156, [0.4588235294117647, 0.4392156862745098, 0.7019607843137254]
color count_Δ156, chain B and (resi 156)
set_color count_T859N, [0.8509803921568627, 0.37254901960784315, 0.00784313725490196]
color count_T859N, chain B and (resi 859)
set_color count_R214ins, [0.4588235294117647, 0.4392156862745098, 0.7019607843137254]
color count_R214ins, chain B and (resi 214)
set_color count_Y489H, [0.10588235294117647, 0.6196078431372549, 0.4666666666666667]
color count_Y489H, chain B and (resi 489)
set_color count_V83A, [0.4588235294117647, 0.4392156862745098, 0.7019607843137254]
color count_V83A, chain B and (resi 83)
set_color count_T478R, [0.10588235294117647, 0.6196078431372549, 0.4666666666666667]
color count_T478R, chain B and (resi 478)
set_color count_Q52R, [0.4588235294117647, 0.4392156862745098, 0.7019607843137254]
color count_Q52R, chain B and (resi 52)
set_color count_D80Y, [0.4588235294117647, 0.4392156862745098, 0.7019607843137254]
color count_D80Y, chain B and (resi 80)
set_color count_Y248N, [0.4588235294117647, 0.4392156862745098, 0.7019607843137254]
color count_Y248N, chain B and (resi 248)
select muts, chain B and (resi 19 or resi 478 or resi 1139 or resi 155 or resi 156 or resi 1112 or resi 152 or resi 145 or resi 142 or resi 658 or resi 222 or resi 156 or resi 859 or resi 214 or resi 489 or resi 83 or resi 478 or resi 52 or resi 80 or resi 248) and n. CA
show spheres, muts
set sphere_scale, 1.3
bg 0
