from flask import Flask, render_template, request, send_file
import re
import os

app = Flask(__name__)

# Load original script
def load_script():
    script_path = "retro.txt"  # Ensure this file is in the same directory
    with open(script_path, "r", encoding="utf-8") as file:
        return file.read()

# Replace placeholders in script
def replace_script(data):
    script = load_script()
    
    replacements = {
        "MeContext=MEL02960": f"MeContext={data['node_id']}",
        "ManagedElement=MEL02960": f"ManagedElement={data['node_id']}",
        "FieldReplaceableUnit=RRU-1": f"FieldReplaceableUnit=RRU-{data.get('rru_number', '1')}",
        "RRU-1": f"RRU-{data.get('rru_number', '1')}",
        r"AntennaUnitGroup=\d+": f"AntennaUnitGroup={data.get('antenna_unit_group', '1')}",
        r"AntennaUnit=\d+": f"AntennaUnit={data.get('antenna_unit', '1')}",
        r"AntennaSubunit=\d+": f"AntennaSubunit={data.get('antenna_subunit', '1')}",
        "rfBranchId : \"1\"": f"rfBranchId : \"{data['rf_branch_existing_1']}\"",
        "rfBranchId : \"2\"": f"rfBranchId : \"{data['rf_branch_existing_2']}\"",
        "rfBranchId : \"3\"": f"rfBranchId : \"{data['rf_branch_new_1']}\"",
        "rfBranchId : \"4\"": f"rfBranchId : \"{data['rf_branch_new_2']}\"",
        "RfBranch=1": f"RfBranch={data.get('rf_branch_existing_1', '1')}",
        "RfBranch=2": f"RfBranch={data.get('rf_branch_existing_2', '2')}",
        "RfBranch=3": f"RfBranch={data.get('rf_branch_new_1', '3')}",
        "RfBranch=4": f"RfBranch={data.get('rf_branch_new_2', '4')}",
        "rfPortId : \"A\"": f"rfPortId : \"{data['rf_port_existing_1']}\"",
        "rfPortId : \"B\"": f"rfPortId : \"{data['rf_port_existing_2']}\"",
        "rfPortId : \"C\"": f"rfPortId : \"{data['rf_port_new_1']}\"",
        "rfPortId : \"D\"": f"rfPortId : \"{data['rf_port_new_2']}\"",
        "RfPort=A": f"RfBranch={data.get('rf_port_existing_1', 'A')}",
        "RfPort=B": f"RfBranch={data.get('rf_port_existing_2', 'B')}",
        "RfPort=C": f"RfBranch={data.get('rf_port_new_1', 'C')}",
        "RfPort=D": f"RfBranch={data.get('rf_port_new_2', 'D')}",
        r"SectorCarrier=\d+": f"SectorCarrier={data['sector_carrier']}",
        r"SectorEquipmentFunction=\d+": f"SectorEquipmentFunction={data['sector_equipment_function']}",
        "EUtranCellFDD=MEL02960_7A_1": f"EUtranCellFDD={data['eutran_cell_fdd']}",
        "configuredMaxTxPower : \"160000\"": f"configuredMaxTxPower : \"{data['max_tx_power']}\""
    }
    
    
    for key, value in replacements.items():
        script = re.sub(key, value, script)
    
    formatted_attenuation = f"[{', '.join([data['attenuation']] * 15)}]"
    formatted_traffic_delay = f"[{', '.join([data['traffic_delay']] * 15)}]"
    script = re.sub(r"dlAttenuation : \[.*?\]", f"dlAttenuation : {formatted_attenuation}", script)
    script = re.sub(r"ulAttenuation : \[.*?\]", f"ulAttenuation : {formatted_attenuation}", script)
    script = re.sub(r"dlTrafficDelay : \[.*?\]", f"dlTrafficDelay : {formatted_traffic_delay}", script)
    script = re.sub(r"ulTrafficDelay : \[.*?\]", f"ulTrafficDelay : {formatted_traffic_delay}", script)
    
    return script

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form.to_dict()
        modified_script = replace_script(data)
        output_file = "modified_retro.txt"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(modified_script)
        return send_file(output_file, as_attachment=True)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
