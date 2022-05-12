from __future__ import annotations
from typing import *
from pydantic import BaseModel, Field
import requests


class AssociationShortInfo(BaseModel):
    account: Optional[str] = Field(None, description='Account name')
    cluster: Optional[str] = Field(None, description='Cluster name')
    partition: Optional[str] = Field(
        None, description='Partition name (optional)')
    user: Optional[str] = Field(None, description='User name')


class CoordinatorInfo(BaseModel):
    name: Optional[str] = Field(None, description='Name of user')
    direct: Optional[int] = Field(
        None,
        description='If user is coordinator of this account directly or coordinator status was inheirted from a higher account in the tree',
    )


class Error(BaseModel):
    error: Optional[str] = Field(None, description='error message')
    errno: Optional[int] = Field(None, description='error number')


class ResponseAccountDelete(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')


class ResponseAssociationDelete(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')


class ResponseClusterAdd(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')


class ResponseClusterDelete(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')


class ResponseQosDelete(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')


class ResponseTres(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')


class ResponseUserDelete(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')


class ResponseUserUpdate(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')


class ResponseWckeyAdd(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')


class ResponseWckeyDelete(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')


class Wckey(BaseModel):
    accounts: Optional[List[str]] = Field(
        None, description='List of assigned accounts')
    cluster: Optional[str] = Field(None, description='Cluster name')
    id: Optional[int] = Field(None, description='wckey database unique id')
    name: Optional[str] = Field(None, description='wckey name')
    user: Optional[str] = Field(None, description='wckey user')
    flags: Optional[List[str]] = Field(
        None, description='List of properties of wckey')


class WckeyInfo(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')
    wckeys: Optional[List[Wckey]] = Field(None, description='List of wckeys')


class AssociationDefault(BaseModel):
    qos: Optional[str] = Field(None, description='Default QOS')


class AssociationMaxJobsPer(BaseModel):
    wall_clock: Optional[int] = Field(
        None, description='Max wallclock per job')


class AssociationMaxPerAccount(BaseModel):
    wall_clock: Optional[int] = Field(
        None, description='Max wallclock per account')


class AssociationMaxTresMinutesPer(BaseModel):
    job: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )


class AssociationMaxTresPer(BaseModel):
    job: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )
    node: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )


class AssociationMin(BaseModel):
    priority_threshold: Optional[int] = Field(
        None, description='Min priority threshold'
    )


class AssociationUsage(BaseModel):
    accrue_job_count: Optional[int] = Field(
        None, description='Jobs accuring priority')
    group_used_wallclock: Optional[int] = Field(
        None, description='Group used wallclock time (s)'
    )
    fairshare_factor: Optional[int] = Field(
        None, description='Fairshare factor')
    fairshare_shares: Optional[int] = Field(
        None, description='Fairshare shares')
    normalized_priority: Optional[int] = Field(
        None, description='Currently active jobs'
    )
    normalized_shares: Optional[int] = Field(
        None, description='Normalized shares')
    effective_normalized_usage: Optional[int] = Field(
        None, description='Effective normalized usage'
    )
    raw_usage: Optional[int] = Field(None, description='Raw usage')
    job_count: Optional[int] = Field(None, description='Total jobs submitted')
    fairshare_level: Optional[int] = Field(None, description='Fairshare level')


class ClusterInfoAssociations(BaseModel):
    root: Optional[AssociationShortInfo] = Field(None, description='')


class ClusterInfoController(BaseModel):
    host: Optional[str] = Field(None, description='Hostname')
    port: Optional[int] = Field(None, description='Port number')


class DiagRollups(BaseModel):
    type: Optional[str] = Field(None, description='Type of rollup')
    last_run: Optional[int] = Field(
        None, description='Timestamp of last rollup')
    last_cycle: Optional[int] = Field(
        None, description='Timestamp of last cycle')
    max_cycle: Optional[int] = Field(
        None, description='Max time of all cycles')
    total_time: Optional[int] = Field(
        None, description='Total time (s) spent doing rollup'
    )
    mean_cycles: Optional[int] = Field(
        None, description='Average time (s) of cycle')


class DiagTime(BaseModel):
    average: Optional[int] = Field(
        None, description='Average time spent processing this RPC type'
    )
    total: Optional[int] = Field(
        None, description='Total time spent processing this RPC type'
    )


class DiagTime1(BaseModel):
    average: Optional[int] = Field(
        None, description='Average time spent processing each user RPC'
    )
    total: Optional[int] = Field(
        None, description='Total time spent processing each user RPC'
    )


class DiagUsers(BaseModel):
    user: Optional[str] = Field(None, description='User name')
    count: Optional[int] = Field(None, description='Number of RPCs')
    time: Optional[DiagTime1] = Field(None, description='')


class JobArrayLimitsMaxRunning(BaseModel):
    tasks: Optional[int] = Field(
        None, description='Max running tasks in array at any one time'
    )


class JobComment(BaseModel):
    administrator: Optional[str] = Field(
        None, description='Administrator set comment')
    job: Optional[str] = Field(None, description='Job comment')
    system: Optional[str] = Field(None, description='System set comment')


class JobExitCodeSignal(BaseModel):
    signal_id: Optional[int] = Field(
        None, description='Signal number process received')
    name: Optional[str] = Field(None, description='Name of signal received')


class JobHet(BaseModel):
    job_id: Optional[Dict[str, Any]] = Field(
        None, description='Parent HetJob id')
    job_offset: Optional[Dict[str, Any]] = Field(
        None, description='Offset of this job to parent'
    )


class JobMcs(BaseModel):
    label: Optional[str] = Field(None, description='Assigned MCS label')


class JobRequired(BaseModel):
    CPUs: Optional[int] = Field(None, description='Required number of CPUs')
    memory: Optional[int] = Field(
        None, description='Required amount of memory (MiB)')


class JobReservation(BaseModel):
    id: Optional[int] = Field(None, description='Database id of reservation')
    name: Optional[int] = Field(None, description='Name of reservation')


class JobState(BaseModel):
    current: Optional[str] = Field(None, description='Current state of job')
    reason: Optional[str] = Field(
        None, description="Last reason job didn't run")


class JobStepCpuRequestedFrequency(BaseModel):
    min: Optional[int] = Field(None, description='Min CPU frequency')
    max: Optional[int] = Field(None, description='Max CPU frequency')


class JobStepNodes(BaseModel):
    count: Optional[int] = Field(
        None, description='Total number of nodes in step')
    range: Optional[str] = Field(None, description='Nodes in step')


class JobStepStatisticsCpu(BaseModel):
    actual_frequency: Optional[int] = Field(
        None, description='Actual frequency of CPU during step'
    )


class JobStepStatisticsEnergy(BaseModel):
    consumed: Optional[int] = Field(
        None, description='Energy consumed during step')


class JobStepStepHet(BaseModel):
    component: Optional[int] = Field(
        None, description='Parent HetJob component id')


class JobStepStepTask(BaseModel):
    distribution: Optional[str] = Field(
        None, description='Task distribution type')


class JobStepStepTresRequested(BaseModel):
    average: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )
    max: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )
    min: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )
    total: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )


class JobStepTasks(BaseModel):
    count: Optional[int] = Field(None, description='Number of tasks in step')


class JobTimeSystem(BaseModel):
    seconds: Optional[int] = Field(
        None,
        description='Total number of CPU-seconds used by the system on behalf of the process (in kernel mode), in seconds',
    )
    microseconds: Optional[int] = Field(
        None,
        description='Total number of CPU-seconds used by the system on behalf of the process (in kernel mode), in microseconds',
    )


class JobTimeTotal(BaseModel):
    seconds: Optional[int] = Field(
        None, description='Total number of CPU-seconds used by the job, in seconds'
    )
    microseconds: Optional[int] = Field(
        None, description='Total number of CPU-seconds used by the job, in microseconds'
    )


class JobTimeUser(BaseModel):
    seconds: Optional[int] = Field(
        None,
        description='Total number of CPU-seconds used by the job in user land, in seconds',
    )
    microseconds: Optional[int] = Field(
        None,
        description='Total number of CPU-seconds used by the job in user land, in microseconds',
    )


class JobTres(BaseModel):
    allocated: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )
    requested: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )


class JobWckey(BaseModel):
    wckey: Optional[str] = Field(None, description='Job assigned wckey')
    flags: Optional[List[str]] = Field(None, description='wckey flags')


class QosLimitsMaxAccruingPer(BaseModel):
    account: Optional[int] = Field(
        None, description='Max accuring priority per account'
    )
    user: Optional[int] = Field(
        None, description='Max accuring priority per user')


class QosLimitsMaxJobsPer(BaseModel):
    account: Optional[int] = Field(None, description='Max jobs per account')
    user: Optional[int] = Field(None, description='Max jobs per user')


class QosLimitsMaxTresMinutesPer(BaseModel):
    job: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )
    account: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )
    user: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )


class QosLimitsMaxTresPer(BaseModel):
    account: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )
    job: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )
    node: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )
    user: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )


class QosLimitsMaxWallClockPer(BaseModel):
    qos: Optional[int] = Field(None, description='Max wallclock per QOS')
    job: Optional[int] = Field(None, description='Max wallclock per job')


class QosLimitsMinTresPer(BaseModel):
    job: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )


class QosPreempt(BaseModel):
    list: Optional[List[str]] = Field(
        None, description='List of preemptable QOS')
    mode: Optional[List[str]] = Field(
        None, description='List of preemption modes')
    exempt_time: Optional[int] = Field(
        None, description='Grace period (s) before jobs can preempted'
    )


class UserAssociations(BaseModel):
    root: Optional[AssociationShortInfo] = Field(None, description='')


class UserDefault(BaseModel):
    account: Optional[str] = Field(None, description='Default account name')
    wckey: Optional[str] = Field(None, description='Default wckey')


class JobProperties(BaseModel):
    account: Optional[str] = Field(
        None, description='Charge resources used by this job to specified account.'
    )
    account_gather_freqency: Optional[str] = Field(
        None, description='Define the job accounting and profiling sampling intervals.'
    )
    argv: Optional[List[str]] = Field(
        None, description='Arguments to the script.')
    array: Optional[str] = Field(
        None,
        description='Submit a job array, multiple jobs to be executed with identical parameters. The indexes specification identifies what array index values should be used.',
    )
    batch_features: Optional[str] = Field(
        None, description="features required for batch script's node"
    )
    begin_time: Optional[int] = Field(
        None,
        description='Submit the batch script to the Slurm controller immediately, like normal, but tell the controller to defer the allocation of the job until the specified time. format: int64',
    )
    burst_buffer: Optional[str] = Field(
        None, description='Burst buffer specification.')
    cluster_constraints: Optional[str] = Field(
        None,
        description='Specifies features that a federated cluster must have to have a sibling job submitted to it.',
    )
    comment: Optional[str] = Field(None, description='An arbitrary comment.')
    constraints: Optional[str] = Field(
        None, description='node features required by job.'
    )
    core_specification: Optional[int] = Field(
        None,
        description='Count of specialized threads per node reserved by the job for system operations and not used by the application.',
    )
    cores_per_socket: Optional[int] = Field(
        None,
        description='Restrict node selection to nodes with at least the specified number of cores per socket.',
    )
    cpu_binding: Optional[str] = Field(None, description='Cpu binding')
    cpu_binding_hint: Optional[str] = Field(
        None, description='Cpu binding hint')
    cpu_frequency: Optional[str] = Field(
        None,
        description='Request that job steps initiated by srun commands inside this sbatch script be run at some requested frequency if possible, on the CPUs selected for the step on the compute node(s).',
    )
    cpus_per_gpu: Optional[str] = Field(
        None, description='Number of CPUs requested per allocated GPU.'
    )
    cpus_per_task: Optional[int] = Field(
        None,
        description='Advise the Slurm controller that ensuing job steps will require ncpus number of processors per task.',
    )
    current_working_directory: Optional[str] = Field(
        None,
        description="Instruct Slurm to connect the batch script's standard output directly to the file name.",
    )
    deadline: Optional[str] = Field(
        None,
        description='Remove the job if no ending is possible before this deadline (start > (deadline - time[-min])).',
    )
    delay_boot: Optional[int] = Field(
        None,
        description="Do not reboot nodes in order to satisfied this job's feature specification if the job has been eligible to run for less than this time period.",
    )
    dependency: Optional[str] = Field(
        None,
        description='Defer the start of this job until the specified dependencies have been satisfied completed.',
    )
    distribution: Optional[str] = Field(
        None, description='Specify alternate distribution methods for remote processes.'
    )
    environment: Optional[Dict[str, Any]] = Field(
        None, description='Dictionary of environment entries.'
    )
    exclusive: Optional[str] = Field(
        None,
        description='The job allocation can share nodes just other users with the "user" option or with the "mcs" option).',
    )
    get_user_environment: Optional[bool] = Field(
        None, description='Load new login environment for user on job node.'
    )
    gres: Optional[str] = Field(
        None,
        description='Specifies a comma delimited list of generic consumable resources.',
    )
    gres_flags: Optional[str] = Field(
        None, description='Specify generic resource task binding options.'
    )
    gpu_binding: Optional[str] = Field(
        None, description='Requested binding of tasks to GPU.'
    )
    gpu_frequency: Optional[str] = Field(
        None, description='Requested GPU frequency.')
    gpus: Optional[str] = Field(None, description='GPUs per job.')
    gpus_per_node: Optional[str] = Field(None, description='GPUs per node.')
    gpus_per_socket: Optional[str] = Field(
        None, description='GPUs per socket.')
    gpus_per_task: Optional[str] = Field(None, description='GPUs per task.')
    hold: Optional[bool] = Field(
        None,
        description='Specify the job is to be submitted in a held state (priority of zero).',
    )
    kill_on_invalid_dependency: Optional[bool] = Field(
        None,
        description='If a job has an invalid dependency, then Slurm is to terminate it.',
    )
    licenses: Optional[str] = Field(
        None,
        description='Specification of licenses (or other resources available on all nodes of the cluster) which must be allocated to this job.',
    )
    mail_type: Optional[str] = Field(
        None, description='Notify user by email when certain event types occur.'
    )
    mail_user: Optional[str] = Field(
        None,
        description='User to receive email notification of state changes as defined by mail_type.',
    )
    mcs_label: Optional[str] = Field(
        None, description='This parameter is a group among the groups of the user.'
    )
    memory_binding: Optional[str] = Field(
        None, description='Bind tasks to memory.')
    memory_per_cpu: Optional[int] = Field(
        None, description='Minimum real memory per cpu (MB).'
    )
    memory_per_gpu: Optional[int] = Field(
        None, description='Minimum memory required per allocated GPU.'
    )
    memory_per_node: Optional[int] = Field(
        None, description='Minimum real memory per node (MB).'
    )
    minimum_cpus_per_node: Optional[int] = Field(
        None, description='Minimum number of CPUs per node.'
    )
    minimum_nodes: Optional[bool] = Field(
        None,
        description='If a range of node counts is given, prefer the smaller count.',
    )
    name: Optional[str] = Field(
        None, description='Specify a name for the job allocation.'
    )
    nice: Optional[str] = Field(
        None,
        description='Run the job with an adjusted scheduling priority within Slurm.',
    )
    no_kill: Optional[bool] = Field(
        None,
        description='Do not automatically terminate a job if one of the nodes it has been allocated fails.',
    )
    nodes: Optional[List[int]] = Field(
        None,
        description='Request that a minimum of minnodes nodes and a maximum node count.',
    )
    open_mode: Optional[str] = Field(
        None,
        description='Open the output and error files using append or truncate mode as specified.',
    )
    partition: Optional[str] = Field(
        None, description='Request a specific partition for the resource allocation.'
    )
    priority: Optional[str] = Field(
        None, description='Request a specific job priority.'
    )
    qos: Optional[str] = Field(
        None, description='Request a quality of service for the job.'
    )
    requeue: Optional[bool] = Field(
        None,
        description='Specifies that the batch job should eligible to being requeue.',
    )
    reservation: Optional[str] = Field(
        None, description='Allocate resources for the job from the named reservation.'
    )
    signal: Optional[str] = Field(
        None,
        description='When a job is within sig_time seconds of its end time, send it the signal sig_num.',
    )
    sockets_per_node: Optional[int] = Field(
        None,
        description='Restrict node selection to nodes with at least the specified number of sockets.',
    )
    spread_job: Optional[bool] = Field(
        None,
        description='Spread the job allocation over as many nodes as possible and attempt to evenly distribute tasks across the allocated nodes.',
    )
    standard_error: Optional[str] = Field(
        None,
        description="Instruct Slurm to connect the batch script's standard error directly to the file name.",
    )
    standard_input: Optional[str] = Field(
        None,
        description="Instruct Slurm to connect the batch script's standard input directly to the file name specified.",
    )
    standard_output: Optional[str] = Field(
        None,
        description="Instruct Slurm to connect the batch script's standard output directly to the file name.",
    )
    tasks: Optional[int] = Field(
        None,
        description='Advises the Slurm controller that job steps run within the allocation will launch a maximum of number tasks and to provide for sufficient resources.',
    )
    tasks_per_core: Optional[int] = Field(
        None, description='Request the maximum ntasks be invoked on each core.'
    )
    tasks_per_node: Optional[int] = Field(
        None, description='Request the maximum ntasks be invoked on each node.'
    )
    tasks_per_socket: Optional[int] = Field(
        None, description='Request the maximum ntasks be invoked on each socket.'
    )
    thread_specification: Optional[int] = Field(
        None,
        description='Count of specialized threads per node reserved by the job for system operations and not used by the application.',
    )
    threads_per_core: Optional[int] = Field(
        None,
        description='Restrict node selection to nodes with at least the specified number of threads per core.',
    )
    time_limit: Optional[int] = Field(None, description='Step time limit.')
    time_minimum: Optional[int] = Field(
        None, description='Minimum run time in minutes.'
    )
    wait_all_nodes: Optional[bool] = Field(
        None, description='Do not begin execution until all nodes are ready for use.'
    )
    wckey: Optional[str] = Field(
        None, description='Specify wckey to be used with job.')


class JobSubmission(BaseModel):
    script: Optional[str] = Field(
        None, description='Executable script (full contents) to run in batch step'
    )
    job: Optional[JobProperties] = Field(None, description='')
    jobs: Optional[List[JobProperties]] = Field(
        None, description='Properties of an HetJob'
    )


class JobSubmissionResponse(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='slurm errors')
    job_id: Optional[int] = Field(None, description='new job ID')
    step_id: Optional[str] = Field(None, description='new job step ID')
    job_submit_user_msg: Optional[str] = Field(
        None, description='Message to user from job_submit plugin'
    )


class Node(BaseModel):
    architecture: Optional[str] = Field(
        None, description='computer architecture')
    burstbuffer_network_address: Optional[str] = Field(
        None, description='BcastAddr')
    boards: Optional[int] = Field(
        None, description='total number of boards per node')
    boot_time: Optional[int] = Field(
        None, description='timestamp of node boot format: int64'
    )
    cores: Optional[int] = Field(
        None, description='number of cores per socket')
    cpu_binding: Optional[int] = Field(
        None, description='Default task binding')
    cpu_load: Optional[int] = Field(
        None, description='CPU load * 100 format: int64')
    free_memory: Optional[int] = Field(None, description='free memory in MiB')
    cpus: Optional[int] = Field(
        None, description='configured count of cpus running on the node'
    )
    features: Optional[str] = Field(None, description='')
    active_features: Optional[str] = Field(
        None, description="list of a node's available features"
    )
    gres: Optional[str] = Field(
        None, description="list of a node's generic resources")
    gres_drained: Optional[str] = Field(
        None, description='list of drained GRES')
    gres_used: Optional[str] = Field(
        None, description='list of GRES in current use')
    mcs_label: Optional[str] = Field(
        None, description='mcs label if mcs plugin in use')
    name: Optional[str] = Field(None, description='node name to slurm')
    next_state_after_reboot: Optional[str] = Field(
        None, description='state after reboot'
    )
    next_state_after_reboot_flags: Optional[List[str]] = Field(
        None, description='node state flags'
    )
    address: Optional[str] = Field(None, description='state after reboot')
    hostname: Optional[str] = Field(None, description="node's hostname")
    state: Optional[str] = Field(None, description='current node state')
    state_flags: Optional[List[str]] = Field(
        None, description='node state flags')
    operating_system: Optional[str] = Field(
        None, description='operating system')
    owner: Optional[str] = Field(
        None, description='User allowed to use this node')
    partitions: Optional[List[str]] = Field(
        None, description='assigned partitions')
    port: Optional[int] = Field(
        None, description='TCP port number of the slurmd')
    real_memory: Optional[int] = Field(
        None, description='configured MB of real memory on the node'
    )
    reason: Optional[str] = Field(
        None, description='reason for node being DOWN or DRAINING'
    )
    reason_changed_at: Optional[int] = Field(
        None, description='Time stamp when reason was set'
    )
    reason_set_by_user: Optional[str] = Field(
        None, description='User that set the reason'
    )
    slurmd_start_time: Optional[int] = Field(
        None, description='timestamp of slurmd startup format: int64'
    )
    sockets: Optional[int] = Field(
        None, description='total number of sockets per node')
    threads: Optional[int] = Field(
        None, description='number of threads per core')
    temporary_disk: Optional[int] = Field(
        None, description='configured MB of total disk in TMP_FS'
    )
    weight: Optional[int] = Field(
        None, description='arbitrary priority of node for scheduling'
    )
    tres: Optional[str] = Field(None, description='TRES on node')
    tres_used: Optional[str] = Field(None, description='TRES used on node')
    tres_weighted: Optional[float] = Field(
        None, description='TRES weight used on node format: double'
    )
    slurmd_version: Optional[str] = Field(None, description='Slurmd version')
    alloc_cpus: Optional[int] = Field(
        None, description='Allocated CPUs format: int64')
    idle_cpus: Optional[int] = Field(
        None, description='Idle CPUs format: int64')
    alloc_memory: Optional[int] = Field(
        None, description='Allocated memory (MB) format: int64'
    )


class NodeAllocation(BaseModel):
    memory: Optional[int] = Field(
        None, description='amount of assigned job memory')
    cpus: Optional[Dict[str, Any]] = Field(
        None, description='amount of assigned job CPUs'
    )
    sockets: Optional[Dict[str, Any]] = Field(
        None, description='assignment status of each socket by socket id'
    )
    cores: Optional[Dict[str, Any]] = Field(
        None, description='assignment status of each core by core id'
    )


class NodesResponse(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='slurm errors')
    nodes: Optional[List[Node]] = Field(None, description='nodes info')


class Partition(BaseModel):
    flags: Optional[List[str]] = Field(None, description='partition options')
    preemption_mode: Optional[List[str]] = Field(
        None, description='preemption type')
    allowed_allocation_nodes: Optional[str] = Field(
        None, description='list names of allowed allocating nodes'
    )
    allowed_accounts: Optional[str] = Field(
        None, description='comma delimited list of accounts'
    )
    allowed_groups: Optional[str] = Field(
        None, description='comma delimited list of groups'
    )
    allowed_qos: Optional[str] = Field(
        None, description='comma delimited list of qos')
    alternative: Optional[str] = Field(
        None, description='name of alternate partition')
    billing_weights: Optional[str] = Field(
        None, description='TRES billing weights')
    default_memory_per_cpu: Optional[int] = Field(
        None, description='default MB memory per allocated CPU format: int64'
    )
    default_time_limit: Optional[int] = Field(
        None, description='default time limit (minutes) format: int64'
    )
    denied_accounts: Optional[str] = Field(
        None, description='comma delimited list of denied accounts'
    )
    denied_qos: Optional[str] = Field(
        None, description='comma delimited list of denied qos'
    )
    preemption_grace_time: Optional[int] = Field(
        None, description='preemption grace time (seconds) format: int64'
    )
    maximum_cpus_per_node: Optional[int] = Field(
        None, description='maximum allocated CPUs per node'
    )
    maximum_memory_per_node: Optional[int] = Field(
        None, description='maximum memory per allocated CPU (MiB) format: int64'
    )
    maximum_nodes_per_job: Optional[int] = Field(
        None, description='Max nodes per job')
    max_time_limit: Optional[int] = Field(
        None, description='Max time limit per job format: int64'
    )
    min_nodes_per_job: Optional[int] = Field(
        None, description='Min number of nodes per job'
    )
    name: Optional[str] = Field(None, description='Partition name')
    nodes: Optional[str] = Field(
        None, description='list names of nodes in partition')
    over_time_limit: Optional[int] = Field(
        None,
        description="job's time limit can be exceeded by this number of minutes before cancellation",
    )
    priority_job_factor: Optional[int] = Field(
        None, description='job priority weight factor'
    )
    priority_tier: Optional[int] = Field(
        None, description='tier for scheduling and preemption'
    )
    qos: Optional[str] = Field(None, description='partition QOS name')
    state: Optional[str] = Field(None, description='Partition state')
    total_cpus: Optional[int] = Field(
        None, description='Total cpus in partition')
    total_nodes: Optional[int] = Field(
        None, description='Total number of nodes in partition'
    )
    tres: Optional[str] = Field(
        None, description='configured TRES in partition')


class PartitionsResponse(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='slurm errors')
    partitions: Optional[List[Partition]] = Field(
        None, description='partition info')


class Ping(BaseModel):
    hostname: Optional[str] = Field(
        None, description='slurm controller hostname')
    ping: Optional[str] = Field(None, description='slurm controller host up')
    mode: Optional[str] = Field(None, description='slurm controller mode')
    status: Optional[int] = Field(None, description='slurm controller status')


class Pings(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='slurm errors')
    pings: Optional[List[Ping]] = Field(
        None, description='slurm controller pings')


class Signal(BaseModel):
    pass


class DiagStatistics(BaseModel):
    parts_packed: Optional[int] = Field(
        None, description='partition records packed')
    req_time: Optional[int] = Field(None, description='generation time')
    req_time_start: Optional[int] = Field(None, description='data since')
    server_thread_count: Optional[int] = Field(
        None, description='Server thread count')
    agent_queue_size: Optional[int] = Field(
        None, description='Agent queue size')
    agent_count: Optional[int] = Field(None, description='Agent count')
    agent_thread_count: Optional[int] = Field(
        None, description='Agent thread count')
    dbd_agent_queue_size: Optional[int] = Field(
        None, description='DBD Agent queue size'
    )
    gettimeofday_latency: Optional[int] = Field(
        None, description='Latency for 1000 calls to gettimeofday()'
    )
    schedule_cycle_max: Optional[int] = Field(
        None, description='Main Schedule max cycle'
    )
    schedule_cycle_last: Optional[int] = Field(
        None, description='Main Schedule last cycle'
    )
    schedule_cycle_total: Optional[int] = Field(
        None, description='Main Schedule cycle iterations'
    )
    schedule_cycle_mean: Optional[int] = Field(
        None, description='Average time for Schedule Max cycle'
    )
    schedule_cycle_mean_depth: Optional[int] = Field(
        None, description='Average depth for Schedule Max cycle'
    )
    schedule_cycle_per_minute: Optional[int] = Field(
        None, description='Main Schedule Cycles per minute'
    )
    schedule_queue_length: Optional[int] = Field(
        None, description='Main Schedule Last queue length'
    )
    jobs_submitted: Optional[int] = Field(None, description='Job submitted')
    jobs_started: Optional[int] = Field(None, description='Job started')
    jobs_completed: Optional[int] = Field(None, description='Job completed')
    jobs_canceled: Optional[int] = Field(None, description='Job cancelled')
    jobs_failed: Optional[int] = Field(None, description='Job failed')
    jobs_pending: Optional[int] = Field(None, description='Job pending')
    jobs_running: Optional[int] = Field(None, description='Job running')
    job_states_ts: Optional[int] = Field(
        None, description='Job states timestamp')
    bf_backfilled_jobs: Optional[int] = Field(
        None, description='Total backfilled jobs (since last slurm start)'
    )
    bf_last_backfilled_jobs: Optional[int] = Field(
        None, description='Total backfilled jobs (since last stats cycle start)'
    )
    bf_backfilled_het_jobs: Optional[int] = Field(
        None, description='Total backfilled heterogeneous job components'
    )
    bf_cycle_counter: Optional[int] = Field(
        None, description='Backfill Schedule Total cycles'
    )
    bf_cycle_mean: Optional[int] = Field(
        None, description='Backfill Schedule Mean cycle'
    )
    bf_cycle_max: Optional[int] = Field(
        None, description='Backfill Schedule Max cycle time'
    )
    bf_last_depth: Optional[int] = Field(
        None, description='Backfill Schedule Last depth cycle'
    )
    bf_last_depth_try: Optional[int] = Field(
        None, description='Backfill Schedule Mean cycle (try sched)'
    )
    bf_depth_mean: Optional[int] = Field(
        None, description='Backfill Schedule Depth Mean'
    )
    bf_depth_mean_try: Optional[int] = Field(
        None, description='Backfill Schedule Depth Mean (try sched)'
    )
    bf_cycle_last: Optional[int] = Field(
        None, description='Backfill Schedule Last cycle time'
    )
    bf_queue_len: Optional[int] = Field(
        None, description='Backfill Schedule Last queue length'
    )
    bf_queue_len_mean: Optional[int] = Field(
        None, description='Backfill Schedule Mean queue length'
    )
    bf_when_last_cycle: Optional[int] = Field(
        None, description='Last cycle timestamp')
    bf_active: Optional[bool] = Field(
        None, description='Backfill Schedule currently active'
    )


class ReservationPurgeCompleted(BaseModel):
    time: Optional[int] = Field(
        None,
        description='amount of seconds this reservation will sit idle until it is revoked',
    )


class ListModel(BaseModel):
    __root__: Any


class Account(BaseModel):
    associations: Optional[List[AssociationShortInfo]] = Field(
        None, description='List of assigned associations'
    )
    coordinators: Optional[List[CoordinatorInfo]] = Field(
        None, description='List of assigned coordinators'
    )
    description: Optional[str] = Field(
        None, description='Description of account')
    name: Optional[str] = Field(None, description='Name of account')
    organization: Optional[str] = Field(
        None, description='Assigned organization of account'
    )
    flags: Optional[List[str]] = Field(
        None, description='List of properties of account'
    )


class Account1(BaseModel):
    associations: Optional[List[AssociationShortInfo]] = Field(
        None, description='List of assigned associations'
    )
    coordinators: Optional[List[CoordinatorInfo]] = Field(
        None, description='List of assigned coordinators'
    )
    description: Optional[str] = Field(
        None, description='Description of account')
    name: Optional[str] = Field(None, description='Name of account')
    organization: Optional[str] = Field(
        None, description='Assigned organization of account'
    )
    flags: Optional[List[str]] = Field(
        None, description='List of properties of account'
    )


class AccountInfo(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')
    accounts: Optional[List[Account1]] = Field(
        None, description='List of accounts')


class AccountResponse(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')


class ClusterInfo(BaseModel):
    controller: Optional[ClusterInfoController] = Field(None, description='')
    flags: Optional[List[str]] = Field(
        None, description='List of properties of cluster'
    )
    name: Optional[str] = Field(None, description='Cluster name')
    nodes: Optional[str] = Field(None, description='Assigned nodes')
    select_plugin: Optional[str] = Field(
        None, description='Configured select plugin')
    associations: Optional[ClusterInfoAssociations] = Field(
        None, description='')
    rpc_version: Optional[int] = Field(None, description='Number rpc version')
    tres: Optional[List[ResponseTres]] = Field(
        None, description='List of TRES in cluster'
    )


class ConfigResponse(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')


class Diag(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='slurm errors')
    statistics: Optional[DiagStatistics] = Field(None, description='')


class JobExitCode(BaseModel):
    status: Optional[str] = Field(None, description='Job exit status')
    return_code: Optional[int] = Field(
        None, description='Return code from parent process'
    )
    signal: Optional[JobExitCodeSignal] = Field(None, description='')


class TresInfo(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')
    tres: Optional[List[ListModel]] = Field(None, description='Array of tres')


class User(BaseModel):
    administrator_level: Optional[str] = Field(
        None, description='Description of administrator level'
    )
    associations: Optional[UserAssociations] = Field(None, description='')
    coordinators: Optional[List[CoordinatorInfo]] = Field(
        None, description='List of assigned coordinators'
    )
    default: Optional[UserDefault] = Field(None, description='')
    name: Optional[str] = Field(None, description='User name')


class UserInfo(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')
    users: Optional[List[User]] = Field(None, description='Array of users')


class AssociationMaxJobs(BaseModel):
    per: Optional[AssociationMaxJobsPer] = Field(None, description='')


class AssociationMaxPer(BaseModel):
    account: Optional[AssociationMaxPerAccount] = Field(None, description='')


class AssociationMaxTresMinutes(BaseModel):
    per: Optional[AssociationMaxTresMinutesPer] = Field(None, description='')
    total: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )


class DiagRpcs(BaseModel):
    rpc: Optional[str] = Field(None, description='RPC type')
    count: Optional[int] = Field(None, description='Number of RPCs')
    time: Optional[DiagTime] = Field(None, description='')


class JobArrayLimitsMax(BaseModel):
    running: Optional[JobArrayLimitsMaxRunning] = Field(None, description='')


class JobStepCpu(BaseModel):
    requested_frequency: Optional[JobStepCpuRequestedFrequency] = Field(
        None, description=''
    )
    governor: Optional[List[str]] = Field(None, description='CPU governor')


class JobStepStatistics(BaseModel):
    CPU: Optional[JobStepStatisticsCpu] = Field(None, description='')
    energy: Optional[JobStepStatisticsEnergy] = Field(None, description='')


class JobStepStepTres(BaseModel):
    requested: Optional[JobStepStepTresRequested] = Field(None, description='')
    consumed: Optional[JobStepStepTresRequested] = Field(None, description='')
    allocated: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )


class JobStepTime(BaseModel):
    elapsed: Optional[int] = Field(None, description='Total time elapsed')
    end: Optional[int] = Field(None, description='Timestamp of when job ended')
    start: Optional[int] = Field(
        None, description='Timestamp of when job started')
    suspended: Optional[int] = Field(
        None, description='Timestamp of when job last suspended'
    )
    system: Optional[JobTimeSystem] = Field(None, description='')
    total: Optional[JobTimeTotal] = Field(None, description='')
    user: Optional[JobTimeUser] = Field(None, description='')


class JobTime(BaseModel):
    elapsed: Optional[int] = Field(None, description='Total time elapsed')
    eligible: Optional[int] = Field(
        None, description='Total time eligible to run')
    end: Optional[int] = Field(None, description='Timestamp of when job ended')
    start: Optional[int] = Field(
        None, description='Timestamp of when job started')
    submission: Optional[int] = Field(
        None, description='Timestamp of when job submitted'
    )
    suspended: Optional[int] = Field(
        None, description='Timestamp of when job last suspended'
    )
    system: Optional[JobTimeSystem] = Field(None, description='')
    total: Optional[JobTimeTotal] = Field(None, description='')
    user: Optional[JobTimeUser] = Field(None, description='')
    limit: Optional[int] = Field(None, description='Job wall clock time limit')


class QosLimitsMaxAccruing(BaseModel):
    per: Optional[QosLimitsMaxAccruingPer] = Field(None, description='')


class QosLimitsMaxJobs(BaseModel):
    per: Optional[QosLimitsMaxJobsPer] = Field(None, description='')


class QosLimitsMaxTresMinutes(BaseModel):
    per: Optional[QosLimitsMaxTresMinutesPer] = Field(None, description='')


class QosLimitsMaxWallClock(BaseModel):
    per: Optional[QosLimitsMaxWallClockPer] = Field(None, description='')


class QosLimitsMinTres(BaseModel):
    per: Optional[QosLimitsMinTresPer] = Field(None, description='')


class JobResources(BaseModel):
    nodes: Optional[str] = Field(
        None, description='list of assigned job nodes')
    allocated_cpus: Optional[int] = Field(
        None, description='number of assigned job cpus'
    )
    allocated_hosts: Optional[int] = Field(
        None, description='number of assigned job hosts'
    )
    allocated_nodes: Optional[List[NodeAllocation]] = Field(
        None, description='node allocations'
    )


class JobResponseProperties(BaseModel):
    account: Optional[str] = Field(
        None, description='Charge resources used by this job to specified account'
    )
    accrue_time: Optional[int] = Field(
        None, description='time job is eligible for running format: int64'
    )
    admin_comment: Optional[str] = Field(
        None, description="administrator's arbitrary comment"
    )
    array_job_id: Optional[str] = Field(
        None, description='job_id of a job array or 0 if N/A'
    )
    array_task_id: Optional[str] = Field(
        None, description='task_id of a job array')
    array_max_tasks: Optional[str] = Field(
        None, description='Maximum number of running array tasks'
    )
    array_task_string: Optional[str] = Field(
        None, description='string expression of task IDs in this record'
    )
    association_id: Optional[str] = Field(
        None, description='association id for job')
    batch_features: Optional[str] = Field(
        None, description="features required for batch script's node"
    )
    batch_flag: Optional[bool] = Field(
        None, description='if batch: queued job with script'
    )
    batch_host: Optional[str] = Field(
        None, description='name of host running batch script'
    )
    flags: Optional[List[str]] = Field(None, description='Job flags')
    burst_buffer: Optional[str] = Field(
        None, description='burst buffer specifications')
    burst_buffer_state: Optional[str] = Field(
        None, description='burst buffer state info'
    )
    cluster: Optional[str] = Field(
        None, description='name of cluster that the job is on'
    )
    cluster_features: Optional[str] = Field(
        None, description='comma separated list of required cluster features'
    )
    command: Optional[str] = Field(None, description='command to be executed')
    comment: Optional[str] = Field(None, description='arbitrary comment')
    contiguous: Optional[bool] = Field(
        None, description='job requires contiguous nodes'
    )
    core_spec: Optional[str] = Field(
        None, description='specialized core count')
    thread_spec: Optional[str] = Field(
        None, description='specialized thread count')
    cores_per_socket: Optional[str] = Field(
        None, description='cores per socket required by job'
    )
    billable_tres: Optional[str] = Field(None, description='billable TRES')
    cpus_per_task: Optional[str] = Field(
        None, description='number of processors required for each task'
    )
    cpu_frequency_minimum: Optional[str] = Field(
        None, description='Minimum cpu frequency'
    )
    cpu_frequency_maximum: Optional[str] = Field(
        None, description='Maximum cpu frequency'
    )
    cpu_frequency_governor: Optional[str] = Field(
        None, description='cpu frequency governor'
    )
    cpus_per_tres: Optional[str] = Field(
        None, description='semicolon delimited list of TRES=# values'
    )
    deadline: Optional[str] = Field(None, description='job start deadline')
    delay_boot: Optional[str] = Field(
        None, description='command to be executed')
    dependency: Optional[str] = Field(
        None, description='synchronize job execution with other jobs'
    )
    derived_exit_code: Optional[str] = Field(
        None, description='highest exit code of all job steps'
    )
    eligible_time: Optional[int] = Field(
        None, description='time job is eligible for running format: int64'
    )
    end_time: Optional[int] = Field(
        None, description='time of termination, actual or expected format: int64'
    )
    excluded_nodes: Optional[str] = Field(
        None, description='comma separated list of excluded nodes'
    )
    exit_code: Optional[int] = Field(None, description='exit code for job')
    features: Optional[str] = Field(
        None, description='comma separated list of required features'
    )
    federation_origin: Optional[str] = Field(
        None, description="Origin cluster's name")
    federation_siblings_active: Optional[str] = Field(
        None, description='string of active sibling names'
    )
    federation_siblings_viable: Optional[str] = Field(
        None, description='string of viable sibling names'
    )
    gres_detail: Optional[List[str]] = Field(None, description='Job flags')
    group_id: Optional[str] = Field(None, description='group job submitted as')
    job_id: Optional[str] = Field(None, description='job ID')
    job_resources: Optional[JobResources] = Field(None, description='')
    job_state: Optional[str] = Field(None, description='state of the job')
    last_sched_evaluation: Optional[str] = Field(
        None, description='last time job was evaluated for scheduling'
    )
    licenses: Optional[str] = Field(
        None, description='licenses required by the job')
    max_cpus: Optional[str] = Field(
        None, description='maximum number of cpus usable by job'
    )
    max_nodes: Optional[str] = Field(
        None, description='maximum number of nodes usable by job'
    )
    mcs_label: Optional[str] = Field(
        None, description='mcs_label if mcs plugin in use')
    memory_per_tres: Optional[str] = Field(
        None, description='semicolon delimited list of TRES=# values'
    )
    name: Optional[str] = Field(None, description='name of the job')
    nodes: Optional[str] = Field(
        None, description='list of nodes allocated to job')
    nice: Optional[str] = Field(None, description='requested priority change')
    tasks_per_core: Optional[str] = Field(
        None, description='number of tasks to invoke on each core'
    )
    tasks_per_socket: Optional[str] = Field(
        None, description='number of tasks to invoke on each socket'
    )
    tasks_per_board: Optional[str] = Field(
        None, description='number of tasks to invoke on each board'
    )
    cpus: Optional[str] = Field(
        None, description='minimum number of cpus required by job'
    )
    node_count: Optional[str] = Field(
        None, description='minimum number of nodes required by job'
    )
    tasks: Optional[str] = Field(None, description='requested task count')
    het_job_id: Optional[str] = Field(
        None, description='job ID of hetjob leader')
    het_job_id_set: Optional[str] = Field(
        None, description='job IDs for all components'
    )
    het_job_offset: Optional[str] = Field(
        None, description='HetJob component offset from leader'
    )
    partition: Optional[str] = Field(
        None, description='name of assigned partition')
    memory_per_node: Optional[str] = Field(
        None, description='minimum real memory per node'
    )
    memory_per_cpu: Optional[str] = Field(
        None, description='minimum real memory per cpu'
    )
    minimum_cpus_per_node: Optional[str] = Field(
        None, description='minimum # CPUs per node'
    )
    minimum_tmp_disk_per_node: Optional[str] = Field(
        None, description='minimum tmp disk per node'
    )
    preempt_time: Optional[int] = Field(
        None, description='preemption signal time format: int64'
    )
    pre_sus_time: Optional[int] = Field(
        None, description='time job ran prior to last suspend format: int64'
    )
    priority: Optional[str] = Field(
        None, description='relative priority of the job')
    profile: Optional[List[str]] = Field(
        None, description='Job profiling requested')
    qos: Optional[str] = Field(None, description='Quality of Service')
    reboot: Optional[bool] = Field(
        None, description='node reboot requested before start'
    )
    required_nodes: Optional[str] = Field(
        None, description='comma separated list of required nodes'
    )
    requeue: Optional[bool] = Field(
        None, description='enable or disable job requeue option'
    )
    resize_time: Optional[int] = Field(
        None, description='time of latest size change format: int64'
    )
    restart_cnt: Optional[str] = Field(
        None, description='count of job restarts')
    resv_name: Optional[str] = Field(None, description='reservation name')
    shared: Optional[str] = Field(
        None, description='type and if job can share nodes with other jobs'
    )
    show_flags: Optional[List[str]] = Field(
        None, description='details requested')
    sockets_per_board: Optional[str] = Field(
        None, description='sockets per board required by job'
    )
    sockets_per_node: Optional[str] = Field(
        None, description='sockets per node required by job'
    )
    start_time: Optional[int] = Field(
        None, description='time execution begins, actual or expected format: int64'
    )
    state_description: Optional[str] = Field(
        None, description='optional details for state_reason'
    )
    state_reason: Optional[str] = Field(
        None, description='reason job still pending or failed'
    )
    standard_error: Optional[str] = Field(
        None, description="pathname of job's stderr file"
    )
    standard_input: Optional[str] = Field(
        None, description="pathname of job's stdin file"
    )
    standard_output: Optional[str] = Field(
        None, description="pathname of job's stdout file"
    )
    submit_time: Optional[int] = Field(
        None, description='time of job submission format: int64'
    )
    suspend_time: Optional[int] = Field(
        None, description='time job last suspended or resumed format: int64'
    )
    system_comment: Optional[str] = Field(
        None, description="slurmctld's arbitrary comment"
    )
    time_limit: Optional[str] = Field(
        None, description='maximum run time in minutes')
    time_minimum: Optional[str] = Field(
        None, description='minimum run time in minutes')
    threads_per_core: Optional[str] = Field(
        None, description='threads per core required by job'
    )
    tres_bind: Optional[str] = Field(
        None, description='Task to TRES binding directives'
    )
    tres_freq: Optional[str] = Field(
        None, description='TRES frequency directives')
    tres_per_job: Optional[str] = Field(
        None, description='semicolon delimited list of TRES=# values'
    )
    tres_per_node: Optional[str] = Field(
        None, description='semicolon delimited list of TRES=# values'
    )
    tres_per_socket: Optional[str] = Field(
        None, description='semicolon delimited list of TRES=# values'
    )
    tres_per_task: Optional[str] = Field(
        None, description='semicolon delimited list of TRES=# values'
    )
    tres_req_str: Optional[str] = Field(
        None, description='tres reqeusted in the job')
    tres_alloc_str: Optional[str] = Field(
        None, description='tres used in the job')
    user_id: Optional[str] = Field(None, description='user id the job runs as')
    user_name: Optional[str] = Field(None, description='user the job runs as')
    wckey: Optional[str] = Field(None, description='wckey for job')
    current_working_directory: Optional[str] = Field(
        None, description='pathname of working directory'
    )


class JobsResponse(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='slurm errors')
    jobs: Optional[List[JobResponseProperties]] = Field(
        None, description='job descriptions'
    )


class Reservation(BaseModel):
    accounts: Optional[str] = Field(None, description='Allowed accounts')
    burst_buffer: Optional[str] = Field(
        None, description='Reserved burst buffer')
    core_count: Optional[int] = Field(
        None, description='Number of reserved cores')
    core_spec_cnt: Optional[int] = Field(
        None, description='Number of reserved specialized cores'
    )
    end_time: Optional[int] = Field(
        None, description='End time of the reservation')
    features: Optional[str] = Field(None, description='List of features')
    flags: Optional[List[str]] = Field(None, description='Reservation options')
    groups: Optional[str] = Field(
        None, description='List of groups permitted to use the reserved nodes'
    )
    licenses: Optional[str] = Field(None, description='List of licenses')
    max_start_delay: Optional[int] = Field(
        None,
        description='Maximum delay in which jobs outside of the reservation will be permitted to overlap once any jobs are queued for the reservation',
    )
    name: Optional[str] = Field(None, description='Reservationn name')
    node_count: Optional[int] = Field(
        None, description='Count of nodes reserved')
    node_list: Optional[str] = Field(
        None, description='List of reserved nodes')
    partition: Optional[str] = Field(None, description='Partition')
    purge_completed: Optional[ReservationPurgeCompleted] = Field(
        None, description='')
    start_time: Optional[int] = Field(
        None, description='Start time of reservation')
    watts: Optional[int] = Field(
        None, description='amount of power to reserve in watts'
    )
    tres: Optional[str] = Field(None, description='List of TRES')
    users: Optional[str] = Field(None, description='List of users')


class ReservationsResponse(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='slurm errors')
    reservations: Optional[List[Reservation]] = Field(
        None, description='reservation info'
    )


class AssociationMaxTres(BaseModel):
    per: Optional[AssociationMaxTresPer] = Field(None, description='')
    total: Optional[List[Dict[str, Any]]] = Field(
        None, description='TRES list of attributes'
    )
    minutes: Optional[AssociationMaxTresMinutes] = Field(None, description='')


class JobArrayLimits(BaseModel):
    max: Optional[JobArrayLimitsMax] = Field(None, description='')


class JobStepStep(BaseModel):
    job_id: Optional[int] = Field(None, description='Parent job id')
    het: Optional[JobStepStepHet] = Field(None, description='')
    id: Optional[str] = Field(None, description='Step id')
    name: Optional[str] = Field(None, description='Step name')
    task: Optional[JobStepStepTask] = Field(None, description='')
    tres: Optional[JobStepStepTres] = Field(None, description='')


class QosLimitsMaxTres(BaseModel):
    minutes: Optional[QosLimitsMaxTresMinutes] = Field(None, description='')
    per: Optional[QosLimitsMaxTresPer] = Field(None, description='')


class QosLimitsMin(BaseModel):
    priority_threshold: Optional[int] = Field(
        None, description='Min priority threshold'
    )
    tres: Optional[QosLimitsMinTres] = Field(None, description='')


class JobStep(BaseModel):
    time: Optional[JobStepTime] = Field(None, description='')
    exit_code: Optional[JobExitCode] = Field(None, description='')
    nodes: Optional[JobStepNodes] = Field(None, description='')
    tasks: Optional[JobStepTasks] = Field(None, description='')
    pid: Optional[str] = Field(None, description='First process PID')
    CPU: Optional[JobStepCpu] = Field(None, description='')
    kill_request_user: Optional[str] = Field(
        None, description='User who requested job killed'
    )
    state: Optional[str] = Field(None, description='State of job step')
    statistics: Optional[JobStepStatistics] = Field(None, description='')
    step: Optional[JobStepStep] = Field(None, description='')


class AssociationMax(BaseModel):
    jobs: Optional[AssociationMaxJobs] = Field(None, description='')
    per: Optional[AssociationMaxPer] = Field(None, description='')
    tres: Optional[AssociationMaxTres] = Field(None, description='')


class JobArray(BaseModel):
    job_id: Optional[int] = Field(None, description='Job id of array')
    limits: Optional[JobArrayLimits] = Field(None, description='')
    task: Optional[str] = Field(None, description='Array task')
    task_id: Optional[int] = Field(None, description='Array task id')


class QosLimitsMax(BaseModel):
    wall_clock: Optional[QosLimitsMaxWallClock] = Field(None, description='')
    jobs: Optional[QosLimitsMaxJobs] = Field(None, description='')
    accruing: Optional[QosLimitsMaxAccruing] = Field(None, description='')
    tres: Optional[QosLimitsMaxTres] = Field(None, description='')


class Association(BaseModel):
    account: Optional[str] = Field(None, description='Assigned account')
    cluster: Optional[str] = Field(None, description='Assigned cluster')
    default: Optional[AssociationDefault] = Field(None, description='')
    flags: Optional[List[str]] = Field(
        None, description='List of properties of association'
    )
    max: Optional[AssociationMax] = Field(None, description='')
    min: Optional[AssociationMin] = Field(None, description='')
    parent_account: Optional[str] = Field(
        None, description='Parent account name')
    partition: Optional[str] = Field(None, description='Assigned partition')
    priority: Optional[int] = Field(None, description='Assigned priority')
    qos: Optional[List[str]] = Field(None, description='Assigned QOS')
    shares_raw: Optional[int] = Field(None, description='Raw fairshare shares')
    usage: Optional[AssociationUsage] = Field(None, description='')
    user: Optional[str] = Field(None, description='Assigned user')


class AssociationsInfo(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')
    associations: Optional[List[Association]] = Field(
        None, description='Array of associations'
    )


class Job(BaseModel):
    account: Optional[str] = Field(None, description='Account charged by job')
    comment: Optional[JobComment] = Field(None, description='')
    allocation_nodes: Optional[str] = Field(
        None, description='Nodes allocated to job')
    array: Optional[JobArray] = Field(None, description='')
    time: Optional[JobTime] = Field(None, description='')
    association: Optional[AssociationShortInfo] = Field(None, description='')
    cluster: Optional[str] = Field(None, description='Assigned cluster')
    constraints: Optional[str] = Field(None, description='Constraints on job')
    derived_exit_code: Optional[JobExitCode] = Field(None, description='')
    exit_code: Optional[JobExitCode] = Field(None, description='')
    flags: Optional[List[str]] = Field(
        None, description='List of properties of job')
    group: Optional[str] = Field(None, description="User's group to run job")
    het: Optional[JobHet] = Field(None, description='')
    job_id: Optional[int] = Field(None, description='Job id')
    name: Optional[str] = Field(None, description='Assigned job name')
    mcs: Optional[JobMcs] = Field(None, description='')
    nodes: Optional[str] = Field(
        None, description='List of nodes allocated for job')
    partition: Optional[str] = Field(
        None, description="Assigned job's partition")
    priority: Optional[int] = Field(None, description='Priority')
    qos: Optional[str] = Field(None, description='Assigned qos name')
    required: Optional[JobRequired] = Field(None, description='')
    kill_request_user: Optional[str] = Field(
        None, description='User who requested job killed'
    )
    reservation: Optional[JobReservation] = Field(None, description='')
    state: Optional[JobState] = Field(None, description='')
    steps: Optional[List[JobStep]] = Field(
        None, description='Job step description')
    tres: Optional[JobTres] = Field(None, description='')
    user: Optional[str] = Field(None, description='Job user')
    wckey: Optional[JobWckey] = Field(None, description='')
    working_directory: Optional[str] = Field(
        None, description='Directory where job was initially started'
    )


class JobInfo(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')
    jobs: Optional[List[Job]] = Field(None, description='Array of jobs')


class QosLimits(BaseModel):
    max: Optional[QosLimitsMax] = Field(None, description='')
    min: Optional[QosLimitsMin] = Field(None, description='')


class Qos(BaseModel):
    description: Optional[str] = Field(None, description='QOS description')
    flags: Optional[List[str]] = Field(
        None, description='List of properties of QOS')
    id: Optional[str] = Field(None, description='Database id')
    limits: Optional[QosLimits] = Field(None, description='')
    preempt: Optional[QosPreempt] = Field(None, description='')
    priority: Optional[int] = Field(None, description='QOS priority')
    usage_factor: Optional[int] = Field(None, description='Usage factor')
    usage_threshold: Optional[int] = Field(None, description='Usage threshold')


class QosInfo(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')
    qos: Optional[List[Qos]] = Field(None, description='Array of QOS')


class ConfigInfo(BaseModel):
    errors: Optional[List[Error]] = Field(None, description='Slurm errors')
    tres: Optional[List[ListModel]] = Field(None, description='Array of TRES')
    accounts: Optional[List[Account1]] = Field(
        None, description='Array of accounts')
    associations: Optional[List[Association]] = Field(
        None, description='Array of associations'
    )
    users: Optional[List[User]] = Field(None, description='Array of users')
    qos: Optional[List[Qos]] = Field(None, description='Array of qos')
    wckeys: Optional[List[Wckey]] = Field(None, description='Array of wckeys')


def openapiGet() -> None:
    """
    Retrieve OpenAPI Specification (openapiGet)


    """
    return requests.get('/openapi')


def openapiJsonGet() -> None:
    """
    Retrieve OpenAPI Specification (openapiJsonGet)


    """
    return requests.get('/openapi.json')


def openapiV3Get() -> None:
    """
    Retrieve OpenAPI Specification (openapiV3Get)


    """
    return requests.get('/openapi/v3')


def openapiYamlGet() -> None:
    """
    Retrieve OpenAPI Specification (openapiYamlGet)


    """
    return requests.get('/openapi.yaml')


def slurmctldCancelJob(job_id, signal=None) -> None:
    """
    cancel or signal job (slurmctldCancelJob)

    :param job_id : Path Parameter — Slurm Job ID default: null format: int64
:param signal=None: Query Parameter — signal to send to job default: null 
    """
    return requests.delete('/slurm/v0.0.37/job/{job_id}')


def slurmctldDiag() -> Diag:
    """
    get diagnostics (slurmctldDiag)


    """
    return requests.get('/slurm/v0.0.37/diag')


def slurmctldGetJob(job_id) -> JobsResponse:
    """
    get job info (slurmctldGetJob)

    :param job_id : Path Parameter — Slurm Job ID default: null format: int64
    """
    return requests.get('/slurm/v0.0.37/job/{job_id}')


def slurmctldGetJobs(update_time=None) -> JobsResponse:
    """
    get list of jobs (slurmctldGetJobs)

    :param update_time=None: Query Parameter — Filter if changed since update_time. Use of this parameter can result in faster replies. default: null format: int64
    """
    return requests.get('/slurm/v0.0.37/jobs')


def slurmctldGetNode(node_name) -> NodesResponse:
    """
    get node info (slurmctldGetNode)

    :param node_name : Path Parameter — Slurm Node Name default: null 
    """
    return requests.get('/slurm/v0.0.37/node/{node_name}')


def slurmctldGetNodes(update_time=None) -> NodesResponse:
    """
    get all node info (slurmctldGetNodes)

    :param update_time=None: Query Parameter — Filter if changed since update_time. Use of this parameter can result in faster replies. default: null format: int64
    """
    return requests.get('/slurm/v0.0.37/nodes')


def slurmctldGetPartition(partition_name, update_time=None) -> PartitionsResponse:
    """
    get partition info (slurmctldGetPartition)

    :param partition_name : Path Parameter — Slurm Partition Name default: null 
:param update_time=None: Query Parameter — Filter if there were no partition changes (not limited to partition in URL endpoint) since update_time. default: null format: int64
    """
    return requests.get('/slurm/v0.0.37/partition/{partition_name}')


def slurmctldGetPartitions(update_time=None) -> PartitionsResponse:
    """
    get all partition info (slurmctldGetPartitions)

    :param update_time=None: Query Parameter — Filter if changed since update_time. Use of this parameter can result in faster replies. default: null format: int64
    """
    return requests.get('/slurm/v0.0.37/partitions')


def slurmctldGetReservation(reservation_name, update_time=None) -> ReservationsResponse:
    """
    get reservation info (slurmctldGetReservation)

    :param reservation_name : Path Parameter — Slurm Reservation Name default: null 
:param update_time=None: Query Parameter — Filter if no reservation (not limited to reservation in URL) changed since update_time. default: null format: int64
    """
    return requests.get('/slurm/v0.0.37/reservation/{reservation_name}')


def slurmctldGetReservations(update_time=None) -> ReservationsResponse:
    """
    get all reservation info (slurmctldGetReservations)

    :param update_time=None: Query Parameter — Filter if changed since update_time. Use of this parameter can result in faster replies. default: null format: int64
    """
    return requests.get('/slurm/v0.0.37/reservations')


def slurmctldPing() -> Pings:
    """
    ping test (slurmctldPing)


    """
    return requests.get('/slurm/v0.0.37/ping')


def slurmctldSubmitJob(job_submission) -> JobSubmissionResponse:
    """
    submit new job (slurmctldSubmitJob)

    :param job_submission : Body Parameter —  
    """
    return requests.post('/slurm/v0.0.37/job/submit')


def slurmctldUpdateJob(job_id, job_properties) -> None:
    """
    update job (slurmctldUpdateJob)

    :param job_id : Path Parameter — Slurm Job ID default: null format: int64
:param job_properties : Body Parameter —  
    """
    return requests.post('/slurm/v0.0.37/job/{job_id}')


def slurmdbdAddClusters() -> ResponseClusterAdd:
    """
    Add clusters (slurmdbdAddClusters)


    """
    return requests.post('/slurmdb/v0.0.37/clusters')


def slurmdbdAddWckeys() -> ResponseWckeyAdd:
    """
    Add wckeys (slurmdbdAddWckeys)


    """
    return requests.post('/slurmdb/v0.0.37/wckeys')


def slurmdbdDeleteAccount(account_name) -> ResponseAccountDelete:
    """
    Delete account (slurmdbdDeleteAccount)

    :param account_name : Path Parameter — Slurm Account Name default: null 
    """
    return requests.delete('/slurmdb/v0.0.37/account/{account_name}')


def slurmdbdDeleteAssociation(cluster=None) -> ResponseAssociationDelete:
    """
    Delete association (slurmdbdDeleteAssociation)

    :param cluster=None: Query Parameter — Cluster name default: null 
    """
    return requests.delete('/slurmdb/v0.0.37/association')


def slurmdbdDeleteCluster(cluster_name) -> ResponseClusterDelete:
    """
    Delete cluster (slurmdbdDeleteCluster)

    :param cluster_name : Path Parameter — Slurm cluster name default: null 
    """
    return requests.delete('/slurmdb/v0.0.37/cluster/{cluster_name}')


def slurmdbdDeleteQos(qos_name) -> ResponseQosDelete:
    """
    Delete QOS (slurmdbdDeleteQos)

    :param qos_name : Path Parameter — Slurm QOS Name default: null 
    """
    return requests.delete('/slurmdb/v0.0.37/qos/{qos_name}')


def slurmdbdDeleteUser(user_name) -> ResponseUserDelete:
    """
    Delete user (slurmdbdDeleteUser)

    :param user_name : Path Parameter — Slurm User Name default: null 
    """
    return requests.delete('/slurmdb/v0.0.37/user/{user_name}')


def slurmdbdDeleteWckey(wckey) -> ResponseWckeyDelete:
    """
    Delete wckey (slurmdbdDeleteWckey)

    :param wckey : Path Parameter — Slurm wckey name default: null 
    """
    return requests.delete('/slurmdb/v0.0.37/wckey/{wckey}')


def slurmdbdDiag() -> Diag:
    """
    Get slurmdb diagnostics (slurmdbdDiag)


    """
    return requests.get('/slurmdb/v0.0.37/diag')


def slurmdbdGetAccount(account_name) -> AccountInfo:
    """
    Get account info (slurmdbdGetAccount)

    :param account_name : Path Parameter — Slurm Account Name default: null 
    """
    return requests.get('/slurmdb/v0.0.37/account/{account_name}')


def slurmdbdGetAccounts() -> AccountInfo:
    """
    Get account list (slurmdbdGetAccounts)


    """
    return requests.get('/slurmdb/v0.0.37/accounts')


def slurmdbdGetAssociation(cluster=None) -> AssociationsInfo:
    """
    Get association info (slurmdbdGetAssociation)

    :param cluster=None: Query Parameter — Cluster name default: null 
    """
    return requests.get('/slurmdb/v0.0.37/association')


def slurmdbdGetAssociations() -> AssociationsInfo:
    """
    Get association list (slurmdbdGetAssociations)


    """
    return requests.get('/slurmdb/v0.0.37/associations')


def slurmdbdGetCluster(cluster_name) -> ClusterInfo:
    """
    Get cluster info (slurmdbdGetCluster)

    :param cluster_name : Path Parameter — Slurm cluster name default: null 
    """
    return requests.get('/slurmdb/v0.0.37/cluster/{cluster_name}')


def slurmdbdGetClusters() -> ClusterInfo:
    """
    Get cluster list (slurmdbdGetClusters)


    """
    return requests.get('/slurmdb/v0.0.37/clusters')


def slurmdbdGetDbConfig() -> ConfigInfo:
    """
    Dump all configuration information (slurmdbdGetDbConfig)


    """
    return requests.get('/slurmdb/v0.0.37/config')


def slurmdbdGetJob(job_id) -> JobInfo:
    """
    Get job info (slurmdbdGetJob)

    :param job_id : Path Parameter — Slurm Job ID default: null format: int64
    """
    return requests.get('/slurmdb/v0.0.37/job/{job_id}')


def slurmdbdGetJobs(submit_time=None) -> JobInfo:
    """
    Get job list (slurmdbdGetJobs)

    :param submit_time=None: Query Parameter — Filter by submission time
Accepted formats:
HH:MM[:SS] [AM|PM]
MMDD[YY] or MM/DD[/YY] or MM.DD[.YY]
MM/DD[/YY]-HH:MM[:SS]
YYYY-MM-DD[THH:MM[:SS]] default: null 
    """
    return requests.get('/slurmdb/v0.0.37/jobs')


def slurmdbdGetQos() -> QosInfo:
    """
    Get QOS list (slurmdbdGetQos)


    """
    return requests.get('/slurmdb/v0.0.37/qos')


def slurmdbdGetSingleQos(qos_name) -> QosInfo:
    """
    Get QOS info (slurmdbdGetSingleQos)

    :param qos_name : Path Parameter — Slurm QOS Name default: null 
    """
    return requests.get('/slurmdb/v0.0.37/qos/{qos_name}')


def slurmdbdGetTres() -> TresInfo:
    """
    Get TRES info (slurmdbdGetTres)


    """
    return requests.get('/slurmdb/v0.0.37/tres')


def slurmdbdGetUser(user_name) -> UserInfo:
    """
    Get user info (slurmdbdGetUser)

    :param user_name : Path Parameter — Slurm User Name default: null 
    """
    return requests.get('/slurmdb/v0.0.37/user/{user_name}')


def slurmdbdGetUsers() -> UserInfo:
    """
    Get user list (slurmdbdGetUsers)


    """
    return requests.get('/slurmdb/v0.0.37/users')


def slurmdbdGetWckey(wckey) -> WckeyInfo:
    """
    Get wckey info (slurmdbdGetWckey)

    :param wckey : Path Parameter — Slurm wckey name default: null 
    """
    return requests.get('/slurmdb/v0.0.37/wckey/{wckey}')


def slurmdbdGetWckeys() -> WckeyInfo:
    """
    Get wckey list (slurmdbdGetWckeys)


    """
    return requests.get('/slurmdb/v0.0.37/wckeys')


def slurmdbdSetDbConfig() -> ConfigResponse:
    """
    Load all configuration information (slurmdbdSetDbConfig)


    """
    return requests.post('/slurmdb/v0.0.37/config')


def slurmdbdUpdateAccount() -> AccountResponse:
    """
    Update accounts (slurmdbdUpdateAccount)


    """
    return requests.post('/slurmdb/v0.0.37/accounts')


def slurmdbdUpdateTres() -> ResponseTres:
    """
    Set TRES info (slurmdbdUpdateTres)


    """
    return requests.post('/slurmdb/v0.0.37/tres')


def slurmdbdUpdateUsers() -> ResponseUserUpdate:
    """
    Update user (slurmdbdUpdateUsers)


    """
    return requests.post('/slurmdb/v0.0.37/users')
