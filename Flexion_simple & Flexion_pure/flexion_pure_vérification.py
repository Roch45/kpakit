import flexion_pure_max

def flexion_pure_vérification(M_Ed, profile, fy, appuis, lo, section_trans):

    M_Rd = flexion_pure_max.flexion_pure_max(profile, fy, appuis, lo, section_trans)

    if M_Ed <= M_Rd:
        return f"✅ Résistance vérifiée\nMoment résistant (M_Rd): {M_Rd:.2f} N.m ≥ Moment appliqué (M_Ed): {M_Ed:.2f} N.m"
    else:
        return f"❌ Résistance non vérifiée\nMoment résistant (M_Rd): {M_Rd:.2f} N.m < Moment appliqué (M_Ed): {M_Ed:.2f} N.m"