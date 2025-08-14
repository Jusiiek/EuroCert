# EuroCert

Aby postawić projekt lokalnie, prosze kierować się Readme z web i api 

[WEB](https://github.com/Jusiiek/EuroCert/blob/main/web/README.md),
[API](https://github.com/Jusiiek/EuroCert/blob/main/api/README.md).


## Hydration error
Przypadek gdzy elementy wyrenderowane po stronie klienta
nie zgadzają się z tym co wysłał serwer (server-rendered HTML).\
Błąd ten może też powstać gdy wywołujemy po stronie serwera 
elementy, które są tylko po stronie klienta np. "LocalStorage".

Kod przed:

```vue

<template>
  <div class="task-counter">
    <p>Aktualny czas: {{ currentTime }}</p>
    <p>Zadania: {{ completedTasks }}/{{ totalTasks }}</p>
    <p>Jesteś online od: {{ onlineTime }}</p>
  </div>
</template>

<script setup>
const currentTime = ref(new Date().toLocaleTimeString())
const onlineTime = ref(new Date().toLocaleTimeString())

onMounted(() => {
  setInterval(() => {
    currentTime.value = new Date().toLocaleTimeString()
  }, 1000)
})

const {tasks} = useTasks()
const completedTasks = computed(() => tasks.value.filter(t => t.completed).length)
const totalTasks = computed(() => tasks.value.length)
</script>

<style scoped>

</style>

```

Aby zapobiegać temu błedowi, wszystko co pokazuję sie po stronie klienta
znaduje się onMounted lub w process.client.

W przypadku dynamicznych wartości zaleca się korzystanie z v-if v-else
np. gdy dane są zaciągane z api. np.

```vue
    <div v-if="isFetching">
        Fetching data...
    </div>
    <div v-else v-for="d in data">...</div>
```

W naszym przypadku, problem dotyczy currentTime i onlineTime. Serwer ma inne wartości niż klient. Wytarczy, że przypisanie nowych wartości umieścimy w onMounted

```vue
<script setup>
import {useTasks} from "~/composables/useTasks";

const currentTime = ref('')
const onlineTime = ref('')

onMounted(() => {
  currentTime.value= new Date().toLocaleTimeString()
  onlineTime.value = new Date().toLocaleTimeString()

  setInterval(() => {
    currentTime.value = new Date().toLocaleTimeString()
  }, 1000)
})

const {tasks} = useTasks()
const completedTasks = computed(() => tasks.value.filter(t => t.completed).length)
const totalTasks = computed(() => tasks.value.length)
</script>
```
