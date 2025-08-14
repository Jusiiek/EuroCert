import { getApiUrl } from "~/services/config";
import { request } from "~/utils/request";
import type { ServiceReturnInterface } from "~/interfaces/services";
import type { CreateUpdateTaskInterface } from "~/interfaces/task";

class Tasks {

    async createTask(body: CreateUpdateTaskInterface): Promise<ServiceReturnInterface> {
        return await request({
            url: `${getApiUrl()}/tasks/`,
            method: "POST",
            body
        })
    }

    async updateTask(body: CreateUpdateTaskInterface, taskId: string): Promise<ServiceReturnInterface> {
        return await request({
            url: `${getApiUrl()}/tasks/${taskId}`,
            method: "PUT",
            body
        })
    }

    async deleteTask(taskId: string): Promise<ServiceReturnInterface> {
        return await request({
            url: `${getApiUrl()}/tasks/${taskId}`,
            method: "DELETE"
        })
    }

    async getUserTasks(): Promise<ServiceReturnInterface> {
        return await request({
            url: `${getApiUrl()}/tasks/`,
        })
    }
}

export const TaskService = new Tasks();