<script setup lang="ts">

const form = reactive({
  title: "",
  description: ""
})

const open = ref(false)

defineShortcuts({
  o: () => open.value = !open.value
})

const emit = defineEmits(["submit"])
async function submitForm() {
  if (!form.title.trim()) {
    alert('Title cannot be empty!')
    return
  }
  emit("submit", {...form})
  open.value = false;
}

async function cancel() {
  form.title = "";
  form.description = "";
  open.value = false;
}

</script>

<template>
  <UModal v-model:open="open">
    <UButton color="primary" variant="solid" title="Add a new task">
      <UIcon name="material-symbols:add-2" class="size-8"/>
    </UButton>

    <template #content>
      <div class="p-3">
        <div class="w-full text-lg text-center mb-3">
          Create a new task
        </div>
        <UForm @submit="submitForm" :state="form" class="w-full">
          <div class="h-[50px]">
            <UInput
                v-model="form.title"
                placeholder="Enter title"
                class="w-full h-full"
            />
          </div>
          <div>
            <UTextarea
                v-model="form.description"
                placeholder="Enter description"
                class="w-full h-full"
            />
          </div>
          <div class="w-full text-lg text-center">
            <UButton
              type="submit"
              class="mt-4 w-auto px-6"
              :disabled="!form.title.length"
              :class="{
                'cursor-pointer': form.title.length
              }"
          >
            Create task
          </UButton>
            <UButton
              color="error"
              class="ml-3 mt-4 w-auto px-6 cursor-pointer"
              @click="cancel"
          >
            Cancel
          </UButton>
          </div>

        </UForm>
      </div>
    </template>
  </UModal>
</template>

<style scoped>

</style>