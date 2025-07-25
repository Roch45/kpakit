import flexion_simple_max

def flexion_simple_vérification(M_Ed, Ved, profile, fy, appuis, lo, section_trans, section_trans2, nature=1, effort_direction=1):

    [M_Rd, Vpl_Rd] = flexion_simple_max.flexion_simple_max(
        profile, fy, appuis, lo, section_trans, section_trans2,
        nature=nature,
        effort_direction=effort_direction
    )

    result_message = ""
    if (M_Ed <= M_Rd) and (Ved <= Vpl_Rd):
        result_message = "✅ Résistance vérifiée\n"
    else:
        result_message = "❌ Résistance non vérifiée\n"
    
    result_message += f"Moment résistant (M_Rd): {M_Rd:.2f} N.m {'≥' if M_Ed <= M_Rd else '<'} Moment appliqué (M_Ed): {M_Ed:.2f} N.m\n"
    result_message += f"Effort tranchant résistant (Vpl_Rd): {Vpl_Rd:.2f} N {'≥' if Ved <= Vpl_Rd else '<'} Effort appliqué (Ved): {Ved:.2f} N"
    
    return result_message