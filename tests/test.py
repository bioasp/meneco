import subprocess
import sys
sys.path.append('../')
from meneco import meneco

# def reaction_ids(prediction):
#     return set([str(p.arg(0)).strip("\"") for p in prediction if p.pred() == "xreaction"])

# def target_ids(prediction):
#     return set([str(p.arg(0)).strip("\"") for p in prediction if p.pred() == "target"])

def test_meneco() : 
    unproducible_targets_result, reconstructable_result, one_min_sol_result, intersection_sol_result, union_sol_result, enumeration_sol_result = meneco.run_meneco('../toy/draft.sbml', '../toy/seeds.sbml', '../toy/targets.sbml', '../toy/repair.sbml', True)
    
    unproducible_targets = set(['M_cu2_c', 'M_dgtp_c', 'M_sheme_c', 'M_cl_c', 'M_2ohph_c', 'M_mlthf_c', 'M_fad_c', 'M_udcpdp_c', 'M_datp_c', 'M_ribflv_c', 'M_mobd_c', 'M_nad_c', 'M_met_DASH_L_c', 'M_gtp_c', 'M_nadp_c', 'M_dctp_c', 'M_10fthf_c', 'M_pe161_c', 'M_thf_c', 'M_pe161_p', 'M_pe160_c', 'M_adp_c', 'M_utp_c', 'M_pheme_c', 'M_cys_DASH_L_c', 'M_pydx5p_c', 'M_amet_c', 'M_fe3_c', 'M_so4_c', 'M_coa_c', 'M_pe160_p'])
    one_min_sol = set(['R_CU2tpp', 'R_CLt3_2pp'])
    union_sol = set(['R_CU2tpp', 'R_CLt3_2pp'])
    intersection_sol = set(['R_CU2tpp', 'R_CLt3_2pp'])
    enumeration_sol = [{'R_CLt3_2pp', 'R_CU2tpp'}]
    reconstructable_sol = ['M_cu2_c', 'M_cl_c']

    # enumeration_sol_result_t = [reaction_ids(l) for l in enumeration_sol_result]

    # print(target_ids(reconstructable_result))
    # print(unproducible_targets_result, reconstructable_result, one_min_sol_result)
    # print(union_sol_result, intersection_sol_result, enumeration_sol_result)
    # print(union_sol_lst, intersection_sol_lst, enumeration_sol_lst)
    assert len(unproducible_targets) == len(unproducible_targets_result)
    assert reconstructable_sol == reconstructable_result
    assert one_min_sol == set(one_min_sol_result)
    assert union_sol == set(union_sol_result)
    assert intersection_sol == set(intersection_sol_result)
    assert enumeration_sol == enumeration_sol_result, print('non')

test_meneco()
