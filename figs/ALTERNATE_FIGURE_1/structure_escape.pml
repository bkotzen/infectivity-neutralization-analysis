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
set_color count_F486S, [0.10588235294117647, 0.6196078431372549, 0.4666666666666667]
color count_F486S, chain B and (resi 486)
set_color count_E484K, [0.10588235294117647, 0.6196078431372549, 0.4666666666666667]
color count_E484K, chain B and (resi 484)
set_color count_F486P, [0.10588235294117647, 0.6196078431372549, 0.4666666666666667]
color count_F486P, chain B and (resi 486)
set_color count_T716F, [0.8509803921568627, 0.37254901960784315, 0.00784313725490196]
color count_T716F, chain B and (resi 716)
set_color count_D574V, [0.8509803921568627, 0.37254901960784315, 0.00784313725490196]
color count_D574V, chain B and (resi 574)
set_color count_Y144del, [0.4588235294117647, 0.4392156862745098, 0.7019607843137254]
color count_Y144del, chain B and (resi 144)
set_color count_K444T, [0.10588235294117647, 0.6196078431372549, 0.4666666666666667]
color count_K444T, chain B and (resi 444)
set_color count_L452R, [0.10588235294117647, 0.6196078431372549, 0.4666666666666667]
color count_L452R, chain B and (resi 452)
set_color count_Q493S, [0.10588235294117647, 0.6196078431372549, 0.4666666666666667]
color count_Q493S, chain B and (resi 493)
set_color count_F490S, [0.10588235294117647, 0.6196078431372549, 0.4666666666666667]
color count_F490S, chain B and (resi 490)
set_color count_S494R, [0.10588235294117647, 0.6196078431372549, 0.4666666666666667]
color count_S494R, chain B and (resi 494)
set_color count_G485R, [0.10588235294117647, 0.6196078431372549, 0.4666666666666667]
color count_G485R, chain B and (resi 485)
set_color count_Q493R, [0.10588235294117647, 0.6196078431372549, 0.4666666666666667]
color count_Q493R, chain B and (resi 493)
set_color count_Δ144, [0.4588235294117647, 0.4392156862745098, 0.7019607843137254]
color count_Δ144, chain B and (resi 144)
set_color count_K417N, [0.10588235294117647, 0.6196078431372549, 0.4666666666666667]
color count_K417N, chain B and (resi 417)
set_color count_T1027I, [0.8509803921568627, 0.37254901960784315, 0.00784313725490196]
color count_T1027I, chain B and (resi 1027)
set_color count_R346T, [0.8509803921568627, 0.37254901960784315, 0.00784313725490196]
color count_R346T, chain B and (resi 346)
set_color count_E484P, [0.10588235294117647, 0.6196078431372549, 0.4666666666666667]
color count_E484P, chain B and (resi 484)
set_color count_G339D, [0.8509803921568627, 0.37254901960784315, 0.00784313725490196]
color count_G339D, chain B and (resi 339)
set_color count_A243del, [0.4588235294117647, 0.4392156862745098, 0.7019607843137254]
color count_A243del, chain B and (resi 243)
select muts, chain B and (resi 486 or resi 484 or resi 486 or resi 716 or resi 574 or resi 144 or resi 444 or resi 452 or resi 493 or resi 490 or resi 494 or resi 485 or resi 493 or resi 144 or resi 417 or resi 1027 or resi 346 or resi 484 or resi 339 or resi 243) and n. CA
show spheres, muts
set sphere_scale, 1.3
bg 0
