"""
Create ansible using a simple interface and various "helper" roles 
which are easier to use than the built in ansible modules

Author: SREIously
"""

from jinja2 import Environment, PackageLoader, select_autoescape
import yaml
import ansible_runner

def main():

    j2env = Environment(
            loader=PackageLoader("auto_ops"),
            autoescape=select_autoescape()
            )

    template = j2env.get_template("playbook.yml")

    print("Enter a name for this action")
    action_name = input()

    print("enter host group")
    inv_group = input()

    print("enter a list of role names")
    roles = dict.fromkeys(input().split(","), {})

    for role in roles:
        with open(f"ansible/roles/{role}/meta/required_vars.yml", 'r') as rf:
            required_vars = yaml.safe_load(rf)

        for var_key, var_type in required_vars.items():
            if type(var_type) == list:
                print(f"Provide value for {var_key} (select from {var_type}):")
            else:
                print(f"Provide value for {var_key} (type={var_type}):")
            roles[role][var_key] = input()
        
    playbook = template.render(action_name=action_name, inv_group=inv_group, roles=roles)
    ansible_runner.run(playbook=playbook)


if __name__ == "__main__":
    main()
