<script setup lang="ts">

import {ref, onMounted} from 'vue'
import {useTasks} from "~/composables/useTasks";

const {tasks, fetchTasks} = useTasks()
const isFetching = ref(false)

onMounted(async () => {
  isFetching.value = true
  try {
    await fetchTasks()
  } finally {
    isFetching.value = false
  }
})

definePageMeta({
  middleware: 'guest'
})

</script>

<template>
  <div class="w-full">
    <div
        v-if="isFetching"
        class="flex items-center justify-center gap-4 h-32"
    >
      <UIcon name="line-md:loading-twotone-loop" class="size-8"/>
      <span class="text-xl">Fetching your data..</span>
    </div>

    <div v-else>
      <div
          v-if="tasks.length === 0"
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
        />
      </div>
    </div>
  </div>
</template>


<style scoped>

</style>