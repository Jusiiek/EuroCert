<script setup lang="ts">
import {ref} from 'vue'
import {useTasks} from "~/composables/useTasks";

interface Props {
  id: string
  title: string
  description?: string
}

const props = defineProps<Props>()

const isEditing = ref(false)
const editedTitle = ref(props.title)
const editedDescription = ref(props.description || '')
const {updateTask, deleteTask} = useTasks()

function startEditing() {
  isEditing.value = true
}

function cancelEditing() {
  editedTitle.value = props.title
  editedDescription.value = props.description || ''
  isEditing.value = false
}

async function removeTask() {
  const confirmed = window.confirm("Are you sure you want to delete this task?");
  if (!confirmed) return;
    await deleteTask(props.id);
}

async function saveTask() {
  if (!editedTitle.value.trim()) {
    alert('Title cannot be empty!')
    return
  }
  await updateTask(props.id, {title: editedTitle.value, description: editedDescription.value})
  isEditing.value = false
}
</script>

<template>
  <UCard class="max-w-md shadow-md">
    <template #header>
      <div v-if="!isEditing" class="text-xl font-bold h-[50px] overflow-auto">
        {{ props.title }}
      </div>
      <div v-else class="h-[50px]">
        <UInput
            v-model="editedTitle"
            placeholder="Enter title"
            class="w-full h-full"
        />
      </div>
    </template>

    <div>
      <div v-if="!isEditing" class="text-gray-700 text-lg h-[120px] overflow-auto">
        {{ props.description || 'No description' }}
      </div>
      <div v-else class="h-[120px]">
        <UTextarea
            v-model="editedDescription"
            placeholder="Enter description"
            class="w-full h-full"
        />
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end space-x-2">
        <UButton
            v-if="!isEditing"
            @click="startEditing"
            size="sm"
            color="primary"
            class="cursor-pointer text-md"
        >
          Edit
        </UButton>
        <UButton
            v-if="!isEditing"
            @click="removeTask"
            size="sm"
            color="error"
            class="cursor-pointer text-md"
        >
          Delete
        </UButton>

        <template v-else>
          <UButton
              @click="saveTask"
              size="sm"
              color="primary"
              class="cursor-pointer text-md"
          >
            Save
          </UButton>
          <UButton
              @click="cancelEditing"
              size="sm"
              color="error"
              variant="outline"
              class="cursor-pointer text-md"
          >
            Cancel
          </UButton>
        </template>
      </div>
    </template>
  </UCard>
</template>
