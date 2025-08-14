<template>
  <div class="w-screen h-screen flex items-center justify-center">
    <UCard class="w-full max-w-md p-6">
      <template #header>
        <h2 class="text-xl font-bold text-center">{{ title }}</h2>
      </template>

      <UForm @submit="submitForm" :state="form" class="flex flex-col items-center">
        <UFormGroup class="w-full mb-4">
          <label for="email" class="block text-md font-medium mb-1 text-gray-400">Email</label>
          <UInput
              id="email"
              v-model="form.email"
              type="email"
              placeholder="Enter your email"
              class="w-full"
          />
        </UFormGroup>

        <UFormGroup class="w-full mb-4">
          <label for="password" class="block text-md font-medium mb-1 text-gray-400">Password</label>
          <UInput
              id="password"
              v-model="form.password"
              :color="showPasswordStrength ? color : 'success'"
              :type="showPassword ? 'text' : 'password'"
              :ui="{ trailing: 'pe-1' }"
              placeholder="Enter your password"
              class="w-full"

          >
            <template #trailing>
              <UButton
                  color="neutral"
                  variant="link"
                  size="sm"
                  :icon="showPassword ? 'i-lucide-eye-off' : 'i-lucide-eye'"
                  :aria-label="showPassword ? 'Hide password' : 'Show password'"
                  :aria-pressed="showPassword"
                  aria-controls="password"
                  @click="showPassword = !showPassword"
              />
            </template>
          </UInput>
        </UFormGroup>


        <div v-if="form.password && form.password.length > 0 && showPasswordStrength">
          <UProgress
              :color="color"
              :indicator="text"
              :model-value="score"
              :max="5"
              size="sm"
          />

          <p id="password-strength" class="text-sm font-medium">
            {{ text }}. Must contain:
          </p>

          <ul class="space-y-1" aria-label="Password requirements">
            <li
                v-for="(req, index) in strength"
                :key="index"
                class="flex items-center gap-0.5"
                :class="req.met ? 'text-success' : 'text-muted'"
            >
              <UIcon :name="req.met ? 'i-lucide-circle-check' : 'i-lucide-circle-x'" class="size-4 shrink-0"/>

              <span class="text-xs font-light">
          {{ req.text }}
          <span class="sr-only">
            {{ req.met ? ' - Requirement met' : ' - Requirement not met' }}
          </span>
        </span>
            </li>
          </ul>
        </div>

        <div class="w-full flex justify-center">
          <UButton
              type="submit"
              class="mt-4 w-auto px-6"
              :disabled="!(form.email.length > 0 && form.password.length > 0)"
              :class="{
                'cursor-pointer': form.email.length > 0 && form.password.length > 0
              }"
          >
            {{ buttonText }}
          </UButton>
        </div>
        <div class="w-full flex justify-center mt-2">
          <NuxtLink :to="linkTarget" class="hover:text-[#05df72]">
            {{ linkLabel }}
          </NuxtLink>
        </div>
      </UForm>
    </UCard>
  </div>
</template>

<script setup>
const props = defineProps({
  title: String,
  buttonText: String,
  linkLabel: String,
  linkTarget: String,
  showPasswordStrength: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(["submit"])
const showPassword = ref(false)

const form = reactive({
  email: "",
  password: ""
})

function checkStrength(str) {
  const requirements = [
    {regex: /.{8,}/, text: 'At least 8 characters'},
    {regex: /\d/, text: 'At least 1 number'},
    {regex: /[a-z]/, text: 'At least 1 lowercase letter'},
    {regex: /[A-Z]/, text: 'At least 1 uppercase letter'},
    {regex: /[!@#$%^&*(),.?":{}|<>]/, text: 'At least 1 special character'}
  ]
  return requirements.map(req => ({met: req.regex.test(str), text: req.text}))
}

const strength = computed(() => checkStrength(form.password))
const score = computed(() => strength.value.filter(req => req.met).length)

const color = computed(() => {
  if (score.value === 0) return 'neutral'
  if (score.value <= 1) return 'error'
  if (score.value <= 3) return 'warning'
  if (score.value === 4) return 'warning'
  return 'success'
})

const text = computed(() => {
  if (score.value === 0) return 'Enter a password'
  if (score.value <= 3) return 'Weak password'
  if (score.value === 4) return 'Medium password'
  return 'Strong password'
})


function submitForm() {
  if (form.email.length > 0 && form.password.length > 0) emit("submit", {...form})
}
</script>

<style scoped>

</style>