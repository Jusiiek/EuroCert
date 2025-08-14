import { ref } from 'vue';
import type {CreateUpdateTaskInterface, TaskInterface} from "~/interfaces/task";
import type { ServiceReturnInterface } from "~/interfaces/services";
import { TaskService } from "~/services/tasks";


export function useTasks() {
    const tasks = ref<TaskInterface[]>([]);

    async function fetchTasks() {
        const { data } = await TaskService.getUserTasks();
        tasks.value = data;
    }

    async function addTask(task: CreateUpdateTaskInterface) {
        const { res, data } = await TaskService.createTask(task);
        await showResult({res, data}, "added");
    }

    async function updateTask(id: string, updated: CreateUpdateTaskInterface) {
        const { res, data } = await TaskService.updateTask(updated, id);
        await showResult({res, data}, "updated");
    }

    async function deleteTask(id: string) {
        const { res, data } = await TaskService.deleteTask(id);
        await showResult({res, data}, "deleted");
    }

    async function showResult(result: ServiceReturnInterface, action: string) {
        const { res, data } = result;
        if (res.status === 200) {
            alert(`Task ${action} successfully.`);
            return
        }
        alert(`Something went wrong. ${data.detail}`);
    }

    const taskCount = computed(() => tasks.value.length);

    return {tasks, taskCount, fetchTasks, addTask, updateTask, deleteTask};
}
