from graphviz import Digraph
from IPython.display import Image, display

def show_biz_arch(file:bool = False):
    # Create a Digraph object
    dot = Digraph('BusinessLayer', format='png')
    dot.attr(rankdir='LR', fontsize='12', labeljust='left')
    # Define styles
    ARCHIMATE_BUSINESS_CAPABILITY = {'shape': 'rectangle', 'style': 'rounded,filled', 'fillcolor': '#fdf6e3',
                                     'fontsize': '10'}
    ARCHIMATE_VALUE_CHAIN_STEP = {'shape': 'parallelogram', 'style': 'filled', 'fillcolor': '#e3f2fd', 'fontsize': '10'}
    LEGEND_STYLE = {'shape': 'rectangle', 'style': 'rounded,dashed', 'fontsize': '10', 'fontcolor': 'gray30'}
    # Top-level header
    dot.attr(label='<<B>Value Chain Overview</B>>', labelloc='t', fontsize='14')
    # Value Chain steps
    value_chain = [
        ("VC1", "Customer Order Placement"),
        ("VC2", "Inventory Check & Reservation"),
        ("VC3", "Order Fulfillment"),
        ("VC4", "Customer Notification"),
    ]
    # Business Capabilities
    capabilities = [
        ("CAP1", "Order Management"),
        ("CAP2", "Inventory Reservation"),
        ("CAP3", "Fulfillment Scheduling"),
        ("CAP4", "Customer Communication"),
    ]
    # Add value chain steps
    for node_id, label in value_chain:
        dot.node(node_id, label, **ARCHIMATE_VALUE_CHAIN_STEP)
    # Add business capabilities
    for node_id, label in capabilities:
        dot.node(node_id, label, **ARCHIMATE_BUSINESS_CAPABILITY)
    # Connect steps in the value chain (linear sequence)
    for i in range(len(value_chain) - 1):
        dot.edge(value_chain[i][0], value_chain[i + 1][0], style='dashed', label='triggers')
    # Connect capabilities to respective value chain steps
    dot.edge("CAP1", "VC1", label='realizes')
    dot.edge("CAP2", "VC2", label='realizes')
    dot.edge("CAP3", "VC3", label='realizes')
    dot.edge("CAP4", "VC4", label='realizes')
    # Add Legend (invisible cluster to keep it clean)
    with dot.subgraph(name='cluster_legend') as legend:
        legend.attr(label='Legend', fontsize='11', style='dashed', color='gray70')
        legend.node('L1', 'Business Capability', **ARCHIMATE_BUSINESS_CAPABILITY)
        legend.node('L2', 'Value Chain Step', **ARCHIMATE_VALUE_CHAIN_STEP)
        legend.edge('L1', 'L2', style='invis')  # Prevents overlap, forces layout

    # Render and view the diagram
    if file:
        dot.render('business_layer_with_legend', view=True)
    else:
        png_bytes = dot.pipe(format='png')
        display(Image(png_bytes))

def show_app_arch():
    from graphviz import Digraph

    dot = Digraph('ApplicationLayerWithInterfaces', format='png')
    dot.attr(rankdir='TB', fontsize='12')

    # Styles
    CAPABILITY_STYLE = {'shape': 'rectangle', 'style': 'rounded,filled', 'fillcolor': '#fdf6e3', 'fontsize': '10'}
    APP_STYLE = {'shape': 'component', 'style': 'filled', 'fillcolor': '#e1f5fe', 'fontsize': '10'}
    REST_IFACE_STYLE = {'shape': 'box', 'style': 'filled', 'fillcolor': '#c8e6c9', 'fontsize': '9'}
    PUBSUB_IFACE_STYLE = {'shape': 'ellipse', 'style': 'filled,dashed', 'fillcolor': '#f8bbd0', 'fontsize': '9'}
    EXT_SYSTEM_STYLE = {'shape': 'cylinder', 'style': 'filled', 'fillcolor': '#f3e5f5', 'fontsize': '10'}

    # Header
    dot.attr(label='<<B>Application Layer with Explicit Interfaces</B>>', labelloc='t', fontsize='14')

    # Capabilities
    capabilities = [
        ("CAP1", "Order Management"),
        ("CAP2", "Inventory Reservation"),
        ("CAP3", "Fulfillment Scheduling"),
        ("CAP4", "Customer Communication"),
    ]
    for node_id, label in capabilities:
        dot.node(node_id, label, **CAPABILITY_STYLE)

    # Applications
    apps = [
        ("APP1", "OrderPortalApp"),
        ("APP2", "InventoryManagerApp"),
        ("APP3", "UserStoreApp"),
    ]
    for node_id, label in apps:
        dot.node(node_id, label, **APP_STYLE)

    # External system
    dot.node("EXT1", "Notification System", **EXT_SYSTEM_STYLE)

    # Application Interfaces (explicit nodes)
    interfaces = [
        ("IF1", "Order API", "REST", "APP1", "APP2"),
        ("IF2", "User Pref API", "REST", "APP2", "APP3"),
        ("IF3", "Notification Topic", "PubSub", "APP2", "EXT1"),
    ]

    for iface_id, label, iface_type, _, _ in interfaces:
        style = REST_IFACE_STYLE if iface_type == "REST" else PUBSUB_IFACE_STYLE
        dot.node(iface_id, f"<<i>{iface_type}</i>>\n{label}", **style)

    # Capability → Application
    dot.edge("CAP1", "APP1", label='serves')
    dot.edge("CAP2", "APP2", label='serves')
    dot.edge("CAP3", "APP2", label='serves')
    dot.edge("CAP4", "APP3", label='serves')

    # App → Interface → Target App/System
    for iface_id, _, _, source_app, target in interfaces:
        dot.edge(source_app, iface_id, label='exposes', style='solid', color='gray30')
        dot.edge(iface_id, target, label='invokes',
                 style='solid' if "IF1" in iface_id or "IF2" in iface_id else 'dashed', color='gray30')

    # Legend
    with dot.subgraph(name='cluster_legend') as legend:
        legend.attr(label='Legend', fontsize='11', style='dashed', color='gray70')
        legend.node('L1', 'Business Capability', **CAPABILITY_STYLE)
        legend.node('L2', 'Application', **APP_STYLE)
        legend.node('L3', 'REST Interface', **REST_IFACE_STYLE)
        legend.node('L4', 'Pub/Sub Interface', **PUBSUB_IFACE_STYLE)
        legend.node('L5', 'External System', **EXT_SYSTEM_STYLE)
        legend.edge('L1', 'L2', style='invis')
        legend.edge('L2', 'L3', style='invis')
        legend.edge('L3', 'L4', style='invis')
        legend.edge('L4', 'L5', style='invis')

    # Render
    png_bytes = dot.pipe(format='png')
    display(Image(png_bytes))

def show_technology_arch():
    from graphviz import Digraph

    dot = Digraph('TechnologyLayer', format='png')
    dot.attr(rankdir='TB', fontsize='12')
    dot.attr(label='<<B>Technology Layer (As-Is)</B>>', labelloc='t', fontsize='14')

    # Styles
    APP_STYLE = {'shape': 'component', 'style': 'filled', 'fillcolor': '#e1f5fe', 'fontsize': '10'}
    INFRA_STYLE = {'shape': 'box3d', 'style': 'filled', 'fillcolor': '#fff3e0', 'fontsize': '10'}
    TECH_STYLE = {'shape': 'cylinder', 'style': 'filled', 'fillcolor': '#f3e5f5', 'fontsize': '10'}
    RUNTIME_STYLE = {'shape': 'note', 'style': 'filled', 'fillcolor': '#ede7f6', 'fontsize': '9'}

    # Applications (same IDs to align with earlier layers)
    dot.node('APP1', 'OrderPortalApp', **APP_STYLE)
    dot.node('APP2', 'InventoryManagerApp', **APP_STYLE)
    dot.node('APP3', 'UserStoreApp', **APP_STYLE)
    dot.node('EXT1', 'Notification System', shape='cylinder', style='filled,dashed', fillcolor='#f8bbd0')

    # Infra components
    infra = [
        ("INF1", "WebLogic Server"),
        ("INF2", "VM on vSphere"),
        ("INF3", "Oracle RDBMS"),
        ("INF4", "MSMQ"),
        ("INF5", "Active Directory"),
        ("INF6", "File Share"),
        ("INF7", "Spring Boot Runtime"),
        ("INF8", "Java 8 (JDK)"),
    ]

    for id, label in infra:
        style = TECH_STYLE if "RDBMS" in label or "MSMQ" in label else INFRA_STYLE
        dot.node(id, label, **style)

    # Add runtimes
    dot.node("R1", "Spring MVC", **RUNTIME_STYLE)
    dot.node("R2", "Spring Boot", **RUNTIME_STYLE)

    # Relationships: Apps deployed on, using tech
    dot.edge("APP1", "INF1", label='deployed on')
    dot.edge("APP1", "INF3", label='uses DB')
    dot.edge("APP1", "R1", label='runs on')
    dot.edge("APP1", "INF8", label='uses JDK')
    dot.edge("APP1", "INF2", label='hosted on')

    dot.edge("APP2", "INF3", label='uses DB')
    dot.edge("APP2", "INF4", label='uses MSMQ')
    dot.edge("APP2", "INF2", label='hosted on')
    dot.edge("APP2", "R2", label='runs on')
    dot.edge("APP2", "INF8", label='uses JDK')

    dot.edge("APP3", "INF1", label='deployed on')
    dot.edge("APP3", "INF3", label='uses DB')
    dot.edge("APP3", "R1", label='runs on')
    dot.edge("APP3", "INF8", label='uses JDK')
    dot.edge("APP3", "INF2", label='hosted on')

    dot.edge("APP1", "INF5", label='auth via')
    dot.edge("APP3", "INF5", label='auth via')

    dot.edge("APP2", "INF6", label='writes to')
    dot.edge("INF4", "EXT1", label='delivers to')

    # Legend
    with dot.subgraph(name='cluster_legend') as legend:
        legend.attr(label='Legend', fontsize='11', style='dashed', color='gray70')
        legend.node('L1', 'Application', **APP_STYLE)
        legend.node('L2', 'Infra Component', **INFRA_STYLE)
        legend.node('L3', 'Platform/DB/Message Bus', **TECH_STYLE)
        legend.node('L4', 'Runtime / Framework', **RUNTIME_STYLE)
        legend.edge('L1', 'L2', style='invis')
        legend.edge('L2', 'L3', style='invis')
        legend.edge('L3', 'L4', style='invis')

    # Render
    from IPython.display import Image, display
    png_bytes = dot.pipe(format='png')
    display(Image(png_bytes))

def show_data_flow():
    from graphviz import Digraph

    dot = Digraph('DataFlowDiagram', format='png')
    dot.attr(rankdir='LR', fontsize='12')
    dot.attr(label='<<B>Data Flow Diagram (As-Is)</B>>', labelloc='t', fontsize='14')

    # Styles
    SYSTEM_STYLE = {'shape': 'box', 'style': 'rounded,filled', 'fillcolor': '#e3f2fd', 'fontsize': '10'}
    ACTOR_STYLE = {'shape': 'oval', 'style': 'filled', 'fillcolor': '#fff3e0', 'fontsize': '10'}
    EXT_STYLE = {'shape': 'box', 'style': 'rounded,filled,dashed', 'fillcolor': '#f3e5f5', 'fontsize': '10'}
    DATA_STYLE = {'shape': 'note', 'style': 'filled', 'fillcolor': '#f1f8e9', 'fontsize': '9'}

    # Nodes
    dot.node('Customer', 'Customer', **ACTOR_STYLE)
    dot.node('OrderPortalApp', 'OrderPortalApp', **SYSTEM_STYLE)
    dot.node('InventoryManagerApp', 'InventoryManagerApp', **SYSTEM_STYLE)
    dot.node('UserStoreApp', 'UserStoreApp', **SYSTEM_STYLE)
    dot.node('NotificationSystem', 'Notification System', **EXT_STYLE)

    # Data objects (optional but great for clarity)
    dot.node('Order', 'Order', **DATA_STYLE)
    dot.node('InventoryInfo', 'Inventory Info', **DATA_STYLE)
    dot.node('UserPrefs', 'User Preferences', **DATA_STYLE)
    dot.node('NotifEvent', 'Notification Event', **DATA_STYLE)

    # Flows
    dot.edge('Customer', 'OrderPortalApp', label='places Order')
    dot.edge('OrderPortalApp', 'Order', label='creates')
    dot.edge('Order', 'InventoryManagerApp', label='for Inventory Check')

    dot.edge('InventoryManagerApp', 'InventoryInfo', label='queries/modifies')
    dot.edge('InventoryManagerApp', 'UserStoreApp', label='requests preferences')
    dot.edge('UserStoreApp', 'UserPrefs', label='provides')
    dot.edge('InventoryManagerApp', 'NotifEvent', label='generates')
    dot.edge('NotifEvent', 'NotificationSystem', label='sends')

    # Optional: direct arrows if you want simpler flow (w/o data nodes)
    # dot.edge('OrderPortalApp', 'InventoryManagerApp', label='Order data')
    # dot.edge('InventoryManagerApp', 'UserStoreApp', label='User ID')
    # dot.edge('InventoryManagerApp', 'NotificationSystem', label='Notify User')

    # Legend (simple)
    with dot.subgraph(name='cluster_legend') as legend:
        legend.attr(label='Legend', fontsize='11', style='dashed', color='gray70')
        legend.node('L1', 'Actor', **ACTOR_STYLE)
        legend.node('L2', 'System', **SYSTEM_STYLE)
        legend.node('L3', 'External System', **EXT_STYLE)
        legend.node('L4', 'Data Entity', **DATA_STYLE)
        legend.edge('L1', 'L2', style='invis')
        legend.edge('L2', 'L3', style='invis')
        legend.edge('L3', 'L4', style='invis')

    # Render
    from IPython.display import Image, display
    png_bytes = dot.pipe(format='png')
    display(Image(png_bytes))

def show_tobe_app_arch():
    dot = Digraph('ToBeApplicationView', format='png')
    dot.attr(rankdir='TB', fontsize='12', size='8.27,11.69!', ratio='fill')  # A4 Portrait
    dot.attr(label='<<B>To-Be Application View (AWS SAM + Lambda)</B>>', labelloc='t', fontsize='14')

    # --- Styles ---
    CAP_STYLE = {'shape': 'rectangle', 'style': 'rounded,filled', 'fillcolor': '#fdf6e3', 'fontsize': '10'}
    APP_STYLE = {'shape': 'component', 'style': 'filled', 'fillcolor': '#e1f5fe', 'fontsize': '10'}
    LAMBDA_STYLE = {'shape': 'box', 'style': 'filled', 'fillcolor': '#dcedc8', 'fontsize': '9'}
    REST_IFACE_STYLE = {'shape': 'note', 'style': 'filled', 'fillcolor': '#c8e6c9', 'fontsize': '9'}
    SNS_IFACE_STYLE = {'shape': 'ellipse', 'style': 'filled,dashed', 'fillcolor': '#f8bbd0', 'fontsize': '9'}

    # --- Business Capabilities ---
    capabilities = [
        ("CAP1", "Order Management"),
        ("CAP2", "Inventory Reservation"),
        ("CAP3", "Fulfillment Scheduling"),
        ("CAP4", "Customer Communication"),
    ]

    for node_id, label in capabilities:
        dot.node(node_id, label, **CAP_STYLE)

    # --- Applications (SAM apps) ---
    sam_apps = [
        ("APP1", "OrderProcessorApp"),
        ("APP2", "InventoryServiceApp"),
        ("APP3", "UserProfileApp"),
        ("APP4", "NotificationService"),
    ]

    for node_id, label in sam_apps:
        dot.node(node_id, label, **APP_STYLE)

    # --- Lambda Functions ---
    lambdas = [
        ("L1", "SubmitOrderFn"),
        ("L2", "ValidateOrderFn"),
        ("L3", "CheckInventoryFn"),
        ("L4", "ReserveStockFn"),
        ("L5", "GetUserPrefsFn"),
        ("L6", "UpdatePrefsFn"),
        ("L7", "NotifyUserFn"),
    ]

    for node_id, label in lambdas:
        dot.node(node_id, label, **LAMBDA_STYLE)

    # --- Interfaces ---
    interfaces = [
        ("IF1", "REST: Submit Order", REST_IFACE_STYLE),
        ("IF2", "REST: Check Inventory", REST_IFACE_STYLE),
        ("IF3", "REST: Get User Prefs", REST_IFACE_STYLE),
        ("IF4", "SNS: Order Events", SNS_IFACE_STYLE),
        ("IF5", "SNS: Notifications", SNS_IFACE_STYLE),
    ]

    for iface_id, label, style in interfaces:
        dot.node(iface_id, label, **style)

    # --- Capability to App connections ---
    dot.edge("CAP1", "APP1", label='served by')
    dot.edge("CAP2", "APP2", label='served by')
    dot.edge("CAP3", "APP2", label='served by')
    dot.edge("CAP4", "APP3", label='served by')
    dot.edge("CAP4", "APP4", label='served by')

    # --- App to Functions ---
    dot.edge("APP1", "L1", label='composes')
    dot.edge("APP1", "L2", label='composes')
    dot.edge("APP2", "L3", label='composes')
    dot.edge("APP2", "L4", label='composes')
    dot.edge("APP3", "L5", label='composes')
    dot.edge("APP3", "L6", label='composes')
    dot.edge("APP4", "L7", label='composes')

    # --- Function to Interfaces ---
    dot.edge("IF1", "L1", label='invokes')  # REST → SubmitOrder
    dot.edge("IF2", "L3", label='invokes')  # REST → CheckInventory
    dot.edge("IF3", "L5", label='invokes')  # REST → GetUserPrefs
    dot.edge("IF4", "L2", label='triggers')  # SNS → ValidateOrder
    dot.edge("IF4", "L4", label='triggers')  # SNS → ReserveStock
    dot.edge("IF5", "L7", label='triggers')  # SNS → NotifyUser

    # --- Legend ---
    with dot.subgraph(name='cluster_legend') as legend:
        legend.attr(label='Legend', fontsize='11', style='dashed', color='gray70')
        legend.node('L_APP', 'Application (SAM)', **APP_STYLE)
        legend.node('L_LAM', 'Lambda Function', **LAMBDA_STYLE)
        legend.node('L_REST', 'REST Interface', **REST_IFACE_STYLE)
        legend.node('L_SNS', 'SNS Topic', **SNS_IFACE_STYLE)
        legend.node('L_CAP', 'Business Capability', **CAP_STYLE)
        legend.edge('L_CAP', 'L_APP', style='invis')
        legend.edge('L_APP', 'L_LAM', style='invis')
        legend.edge('L_LAM', 'L_REST', style='invis')
        legend.edge('L_REST', 'L_SNS', style='invis')

    # Render
    from IPython.display import Image, display
    png_bytes = dot.pipe(format='png')
    display(Image(png_bytes))

def show_tobe_tech_arch():
    from graphviz import Digraph

    dot = Digraph('ToBeTechnologyLayerIcons', format='png')
    dot.attr(rankdir='TB', fontsize='12', size='8.27,11.69!', ratio='fill')
    dot.attr(label='<<B>To-Be Technology Layer (AWS Cloud – Icon View)</B>>', labelloc='t', fontsize='14')

    # --- Style Constants ---
    APP_STYLE = {'shape': 'component', 'style': 'filled', 'fillcolor': '#e1f5fe', 'fontsize': '10'}
    RUNTIME_STYLE = {'shape': 'note', 'style': 'filled', 'fillcolor': '#ede7f6', 'fontsize': '9'}

    # --- Applications ---
    apps = [
        ("APP1", "OrderProcessorApp"),
        ("APP2", "InventoryServiceApp"),
        ("APP3", "UserProfileApp"),
        ("APP4", "NotificationService"),
    ]

    for id, label in apps:
        dot.node(id, label, **APP_STYLE)

    # --- Runtimes ---
    dot.node("RT1", "Python 3.12 Runtime", **RUNTIME_STYLE)

    # --- AWS Icon Nodes (image + label) ---
    aws_services = {
        "T1": (
        "AWS Lambda", "icons/Architecture-Service-Icons_02072025/Arch_Compute/32/Arch_AWS-Lambda_32.png"),
        "T2": ("API Gateway",
               "icons/Architecture-Service-Icons_02072025/Arch_Networking-Content-Delivery/32/Arch_Amazon-API-Gateway_32.png"),
        "T3": ("Amazon SNS",
               "icons/Architecture-Service-Icons_02072025/Arch_App-Integration/32/Arch_Amazon-Simple-Notification-Service_32.png"),
        "T4": (
        "Amazon DynamoDB", "icons/Architecture-Service-Icons_02072025/Arch_Database/32/Arch_Amazon-DynamoDB_32.png"),
        "T5": ("Amazon Cognito",
               "icons/Architecture-Service-Icons_02072025/Arch_Security-Identity-Compliance/32/Arch_Amazon-Cognito_32.png"),
        "T6": ("CloudWatch Logs",
               "icons/Architecture-Service-Icons_02072025/Arch_Management-Governance/32/Arch_Amazon-CloudWatch_32.png"),
    }

    for id, (label, icon_path) in aws_services.items():
        dot.node(id, label='', image=icon_path, shape='none', labelloc='b', width='0.8', height='0.8', xlabel=label)

    # --- App ↔ AWS Tech edges ---
    dot.edge("APP1", "T1")  # Lambda
    dot.edge("APP1", "T2")  # API Gateway
    dot.edge("APP1", "T3")  # SNS
    dot.edge("APP1", "T4")  # Dynamo
    dot.edge("APP1", "T5")  # Cognito
    dot.edge("APP1", "T6")  # CloudWatch
    dot.edge("APP1", "RT1")

    dot.edge("APP2", "T1")
    dot.edge("APP2", "T3")
    dot.edge("APP2", "T4")
    dot.edge("APP2", "T6")
    dot.edge("APP2", "RT1")

    dot.edge("APP3", "T1")
    dot.edge("APP3", "T2")
    dot.edge("APP3", "T4")
    dot.edge("APP3", "T5")
    dot.edge("APP3", "T6")
    dot.edge("APP3", "RT1")

    dot.edge("APP4", "T1")
    dot.edge("APP4", "T3")
    dot.edge("APP4", "T6")
    dot.edge("APP4", "RT1")

    # --- Optional: AWS Cloud boundary grouping ---
    with dot.subgraph(name='cluster_aws_cloud') as aws:
        aws.attr(label='AWS Cloud', style='dashed', color='gray70')
        for aws_id in aws_services:
            aws.node(aws_id)

    # --- Legend (only if needed) ---
    # dot.node("L1", "App", **APP_STYLE)
    # dot.node("L2", "Runtime", **RUNTIME_STYLE)

    # --- Render ---
    from IPython.display import Image, display
    png_bytes = dot.pipe(format='png')
    display(Image(png_bytes))

def show_sidebyside_view():
    from graphviz import Digraph

    dot = Digraph('ComparisonView', format='png')
    dot.attr(rankdir='LR', fontsize='11', size='8.27,11.69!', ratio='compress')
    dot.attr(label="As-Is -> To-Be Application & Technology Comparison View", labelloc='t', fontsize='14')



    # --- Styles ---
    APP_ASIS_STYLE = {'shape': 'component', 'style': 'filled', 'fillcolor': '#ffe0b2', 'fontsize': '10'}
    APP_TOBE_STYLE = {'shape': 'component', 'style': 'filled', 'fillcolor': '#c8e6c9', 'fontsize': '10'}
    TECH_ASIS_STYLE = {'shape': 'box3d', 'style': 'filled', 'fillcolor': '#ffe0e0', 'fontsize': '10'}
    TECH_TOBE_STYLE = {'shape': 'cylinder', 'style': 'filled', 'fillcolor': '#dcedc8', 'fontsize': '10'}

    # --- As-Is Applications ---
    asis_apps = [
        ("A1", "OrderPortalApp"),
        ("A2", "InventoryManagerApp"),
        ("A3", "UserStoreApp"),
        ("A4", "Notification System"),
    ]
    for id, label in asis_apps:
        dot.node("ASIS_" + id, label, **APP_ASIS_STYLE)

    # --- To-Be Applications ---
    tobe_apps = [
        ("A1", "OrderProcessorApp"),
        ("A2", "InventoryServiceApp"),
        ("A3", "UserProfileApp"),
        ("A4", "NotificationService"),
    ]
    for id, label in tobe_apps:
        dot.node("TOBE_" + id, label, **APP_TOBE_STYLE)

    # --- As-Is Tech ---
    asis_tech = [
        ("T1", "WebLogic"),
        ("T2", "Oracle RDBMS"),
        ("T3", "MSMQ"),
        ("T4", "File Share"),
    ]
    for id, label in asis_tech:
        dot.node("ASIS_" + id, label, **TECH_ASIS_STYLE)

    # --- To-Be Tech ---
    tobe_tech = [
        ("T1", "AWS Lambda"),
        ("T2", "DynamoDB"),
        ("T3", "SNS"),
        ("T4", "Amazon S3"),
    ]
    for id, label in tobe_tech:
        dot.node("TOBE_" + id, label, **TECH_TOBE_STYLE)

    # --- Application Mappings (TO-BE replaces AS-IS) ---
    dot.edge("TOBE_A1", "ASIS_A1", label="replaces")
    dot.edge("TOBE_A2", "ASIS_A2", label="replaces")
    dot.edge("TOBE_A3", "ASIS_A3", label="replaces")
    dot.edge("TOBE_A4", "ASIS_A4", label="replaces")

    dot.edge("TOBE_T1", "ASIS_T1", label="replaces")
    dot.edge("TOBE_T2", "ASIS_T2", label="replaces")
    dot.edge("TOBE_T3", "ASIS_T3", label="replaces")
    dot.edge("TOBE_T4", "ASIS_T4", label="replaces")

    # --- Optional: Grouping by clusters ---
    with dot.subgraph(name='cluster_asis') as c1:
        c1.attr(label='As-Is Layer', style='dashed', color='gray70')
        for id, _ in asis_apps + asis_tech:
            c1.node("ASIS_" + id)

    with dot.subgraph(name='cluster_tobe') as c2:
        c2.attr(label='To-Be Layer', style='dashed', color='gray70')
        for id, _ in tobe_apps + tobe_tech:
            c2.node("TOBE_" + id)

    # --- Render ---
    from IPython.display import Image, display
    png_bytes = dot.pipe(format='png')
    display(Image(png_bytes))

def show_roadmap():
    from graphviz import Digraph

    dot = Digraph('Roadmap', format='png')
    dot.attr(rankdir='LR', fontsize='12', size='8.27,11.69!', ratio='compress')
    dot.attr(label='<<B>Roadmap</B>>', labelloc='t', fontsize='14')

    # Styles
    TASK_STYLE = {'shape': 'box', 'style': 'filled', 'fillcolor': '#e1f5fe', 'fontsize': '10'}
    MILESTONE_STYLE = {'shape': 'diamond', 'style': 'filled', 'fillcolor': '#ffe0b2', 'fontsize': '10'}

    # Tasks
    tasks = [
        ("T1", "Requirement Gathering"),
        ("T2", "Design Phase"),
        ("T3", "Development Phase"),
        ("T4", "Testing Phase"),
        ("T5", "Deployment Phase"),
        ("T6", "Post-Deployment Review"),
    ]

    for id, label in tasks:
        dot.node(id, label, **TASK_STYLE)

    # Milestones
    milestones = [
        ("M1", "Phase 1 Complete"),
        ("M2", "Phase 2 Complete"),
        ("M3", "Project Complete"),
    ]

    for id, label in milestones:
        dot.node(id, label, **MILESTONE_STYLE)

    # Task Dependencies
    dot.edge("T1", "T2")
    dot.edge("T2", "M1")
    dot.edge("T2", "T3")
    dot.edge("T3", "M2")
    dot.edge("T3", "T4")
    dot.edge("T4", "M3")
    dot.edge("T4", "T5")
    dot.edge("T5", "M3")
    dot.edge("M1", "T6")

    # Render
    dot.render('roadmap_diagram', view=True)

def show_roadmap_plot():
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    import pandas as pd

    # Extended roadmap: applications + technologies
    data = [
        # Applications
        ("OrderPortalApp", "Deployed", "2025-05-01", "2025-05-31", "As-Is"),
        ("OrderPortalApp", "Phased Out", "2025-06-01", "2025-06-15", "As-Is"),
        ("OrderProcessorApp", "Development", "2025-05-01", "2025-05-31", "To-Be"),
        ("OrderProcessorApp", "Parallel Run", "2025-06-01", "2025-06-30", "To-Be"),
        ("OrderProcessorApp", "Go Live", "2025-07-01", "2025-10-01", "To-Be"),

        ("InventoryManagerApp", "Deployed", "2025-05-01", "2025-05-31", "As-Is"),
        ("InventoryManagerApp", "Phased Out", "2025-06-01", "2025-06-15", "As-Is"),
        ("InventoryServiceApp", "Development", "2025-05-01", "2025-05-31", "To-Be"),
        ("InventoryServiceApp", "Parallel Run", "2025-06-01", "2025-06-30", "To-Be"),
        ("InventoryServiceApp", "Go Live", "2025-07-01", "2025-10-01", "To-Be"),

        ("UserStoreApp", "Deployed", "2025-05-01", "2025-05-31", "As-Is"),
        ("UserStoreApp", "Phased Out", "2025-06-01", "2025-06-15", "As-Is"),
        ("UserProfileApp", "Development", "2025-05-01", "2025-05-31", "To-Be"),
        ("UserProfileApp", "Parallel Run", "2025-06-01", "2025-06-30", "To-Be"),
        ("UserProfileApp", "Go Live", "2025-07-01", "2025-10-01", "To-Be"),

        ("Notification System", "Deployed", "2025-05-01", "2025-05-31", "As-Is"),
        ("Notification System", "Phased Out", "2025-06-01", "2025-06-15", "As-Is"),
        ("NotificationService", "Development", "2025-05-01", "2025-05-31", "To-Be"),
        ("NotificationService", "Parallel Run", "2025-06-01", "2025-06-30", "To-Be"),
        ("NotificationService", "Go Live", "2025-07-01", "2025-10-01", "To-Be"),

        # Technologies
        ("WebLogic", "Active", "2025-05-01", "2025-06-15", "As-Is"),
        ("AWS Lambda", "Rollout", "2025-05-15", "2025-07-15", "To-Be"),

        ("Oracle RDBMS", "Active", "2025-05-01", "2025-06-15", "As-Is"),
        ("DynamoDB", "Rollout", "2025-05-15", "2025-07-15", "To-Be"),

        ("MSMQ", "Active", "2025-05-01", "2025-06-15", "As-Is"),
        ("SNS", "Rollout", "2025-05-15", "2025-07-15", "To-Be"),

        ("File Share", "Active", "2025-05-01", "2025-06-15", "As-Is"),
        ("Amazon S3", "Rollout", "2025-05-15", "2025-07-15", "To-Be"),
    ]

    # Create dataframe
    df = pd.DataFrame(data, columns=["Component", "Phase", "Start", "End", "Type"])
    df["Start"] = pd.to_datetime(df["Start"])
    df["End"] = pd.to_datetime(df["End"])
    df["Duration"] = (df["End"] - df["Start"]).dt.days

    # Setup the plot
    fig, ax = plt.subplots(figsize=(14, 10))

    colors = {
        "As-Is": "#FFAB91",  # soft red
        "To-Be": "#A5D6A7"  # soft green
    }

    yticks = []
    ylabels = []

    # Draw bars
    for i, (comp, group) in enumerate(df.groupby("Component")):
        for _, row in group.iterrows():
            ax.barh(i, row["Duration"], left=row["Start"], color=colors[row["Type"]], edgecolor='black')
            ax.text(row["Start"] + pd.Timedelta(days=1), i, row["Phase"], va='center', ha='left', fontsize=8)
        yticks.append(i)
        ylabels.append(comp)

    # Customize axes
    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels)
    ax.invert_yaxis()
    ax.set_xlabel("Timeline")
    ax.set_title("Full Transition Roadmap (Applications + Technologies)")
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)

    # Legend
    legend_handles = [Patch(color=color, label=label) for label, color in colors.items()]
    ax.legend(handles=legend_handles, loc='upper right')

    plt.tight_layout()
    plt.show()





