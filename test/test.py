from meneco import meneco
import subprocess
import sys
sys.path.append('../')


def reaction_ids(prediction):
    return set([str(p.arg(0)).strip("\"") for p in prediction if p.pred() == "xreaction"])


def test_meneco():
    result = meneco.run_meneco(
        '../toy/draft.sbml', '../toy/seeds.sbml', '../toy/targets.sbml', '../toy/repair.sbml', True, json=True)

    unproducible_targets = ['M_cu2_c', 'M_dgtp_c', 'M_sheme_c', 'M_cl_c', 'M_2ohph_c', 'M_mlthf_c', 'M_fad_c', 'M_udcpdp_c', 'M_datp_c', 'M_ribflv_c', 'M_mobd_c', 'M_nad_c', 'M_met_DASH_L_c', 'M_gtp_c', 'M_nadp_c',
                            'M_dctp_c', 'M_10fthf_c', 'M_pe161_c', 'M_thf_c', 'M_pe161_p', 'M_pe160_c', 'M_adp_c', 'M_utp_c', 'M_pheme_c', 'M_cys_DASH_L_c', 'M_pydx5p_c', 'M_amet_c', 'M_fe3_c', 'M_so4_c', 'M_coa_c', 'M_pe160_p']
    one_min_sol = ['R_CU2tpp', 'R_CLt3_2pp']
    union_sol = ['R_CU2tpp', 'R_CLt3_2pp']
    intersection_sol = ['R_CU2tpp', 'R_CLt3_2pp']
    enumeration_sol = set(['R_CLt3_2pp', 'R_CU2tpp'])

    # enumeration_sol_result_t = [reaction_ids(
    #     l) for l in enumeration_sol_result]

    # print(unproducible_targets_result, reconstructable_result, one_min_sol_result)
    # print(union_sol_result, intersection_sol_result, enumeration_sol_result)
    # print(union_sol_lst, intersection_sol_lst, enumeration_sol_lst)
    assert len(unproducible_targets) == len(result['Unproducible targets'])
    assert one_min_sol == reaction_ids(result['One minimal completion'])
    assert union_sol == reaction_ids(
        result['Union of cardinality minimal completions'])
    assert intersection_sol == reaction_ids(
        result['Intersection of cardinality minimal completions'])
    assert enumeration_sol == set(
        result['All cardinality minimal completions'][0])


test_meneco()
