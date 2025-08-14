<script setup lang="ts">

import {ref, onMounted} from 'vue'
import {useTasks} from "~/composables/useTasks";
import type {CreateUpdateTaskInterface} from "~/interfaces/task";

definePageMeta({
  middleware: 'guest'
})

const {tasks, taskCount, fetchTasks, updateTask, deleteTask, addTask} = useTasks()
const isFetching = ref(false)

async function getUserTasks() {
  isFetching.value = true
  await fetchTasks();
  isFetching.value = false
}

onMounted(async () => {
  await getUserTasks();
})

async function handleTaskCreation(createdBody: CreateUpdateTaskInterface) {
  await addTask(createdBody)
  await getUserTasks();
}

async function handleTaskUpdated(taskId: string, updatedBody: CreateUpdateTaskInterface) {
  await updateTask(taskId, updatedBody)
  await getUserTasks();

}

async function handleDeleteTask(taskId: string) {
  await deleteTask(taskId)
  await getUserTasks();
}

</script>

<template>
  <div class="w-full">
    <div class="w-full flex items-center justify-between px-4">
      <div class="flex-1 text-center">
        <span v-if="!isFetching" class="text-xl">You have: {{ taskCount }}</span>
      </div>
      <task-creation-modal @submit="handleTaskCreation"/>
    </div>
    <div
        v-if="isFetching"
        class="flex items-center justify-center gap-4 h-32"
    >
      <UIcon name="line-md:loading-twotone-loop" class="size-8"/>
      <span class="text-xl">Fetching your data..</span>
    </div>

    <div v-else>
      <div
          v-if="taskCount === 0"
          class="flex items-center justify-center gap-4 h-32 text-xl"
      >
        No tasks have been created yet.
      </div>

      <div v-else class="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 p-4">
        <TaskCard
            v-for="task in tasks"
            :key="task._id"
            :id="task._id"
            :title="task.title"
            :description="task.description"
            @update="handleTaskUpdated"
            @delete="handleDeleteTask"
        />
      </div>
    </div>
  </div>
</template>
<style scoped>

</style>