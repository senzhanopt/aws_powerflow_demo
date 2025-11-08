import json
import numpy as np
import pandas as pd
from grid_feedback_optimizer.engine.powerflow import PowerFlowSolver
from grid_feedback_optimizer.models.loader import load_network


def main():

    # Load JSON file
    network = load_network("data/grid.json")
    power_flow_solver = PowerFlowSolver(network)

    # base profile
    gen_base_p = np.array([g.p_norm for g in network.renew_gens])
    gen_base_q = np.array([g.q_norm for g in network.renew_gens])
    gen_base = np.column_stack((gen_base_p, gen_base_q))
    load_base_p = np.array([l.p_norm for l in network.loads])
    load_base_q = np.array([l.q_norm for l in network.loads])
    load_base = np.column_stack((load_base_p, load_base_q))

    # load scenarios
    scenario = pd.read_csv("data/scenario.csv")

    is_congested: dict = {}
    for i, s in enumerate(scenario.scenario_id):
        output_data = power_flow_solver.run(
            gen_update=scenario.gen_scale[i] * gen_base,
            load_update=scenario.load_scale[i] * load_base
        )
        is_congested[i] = power_flow_solver.is_congested(output_data)
    
    # save results to json
    with open("data/is_congested.json", "w") as f:
        json.dump(is_congested, f, indent=4)

    print("✅ Congestion results saved to data/is_congested.json")


if __name__ == "__main__":
    main()