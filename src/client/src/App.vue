<script setup lang="ts">
import { ref, computed } from "vue";

interface MatchItem {
  name: string,
  sim: number,
}

const ms_remaining = ref(5000);
const json_data = ref([] as MatchItem[]);
const match_result = computed(() => {
  const total_sim = json_data.value.reduce((pre, cur) => pre + cur.sim, 0) + 0.2;
  return {
    unmatched: 0.2 / total_sim,
    top: json_data.value.map(item => {
      return {
        name: item.name,
        sim: item.sim / total_sim
      };
    }).slice(0, 3),
  };
});

function upload_audio(e: BlobEvent, audio_recorder: MediaRecorder) {
  e.data.arrayBuffer().then(buffer => {
    const base64String = btoa(String.fromCharCode(...new Uint8Array(buffer)));
    return fetch("/api/v1/match", {
      body: JSON.stringify({
        audio_base64: base64String,
        app_type: e.data.type,
      }),
      headers: { "Content-Type": "application/json" },
      method: "POST",
    });
  }).then(response => {
    return response.json()
  }).then(data => {
    json_data.value = data;
    audio_recorder.start();
  });
}

navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
  const audio_recorder = new MediaRecorder(stream);
  audio_recorder.start();
  setInterval(() => {
    ms_remaining.value -= 100;
    if (ms_remaining.value <= 0) {
      audio_recorder.stop();
      ms_remaining.value = 5000;
    }
  }, 100);
  audio_recorder.ondataavailable = e => upload_audio(e, audio_recorder);
});
</script>

<template>
  <div>
    {{ ms_remaining }} / 5000
  </div>
  <div>
    <div class="item">
      <span>Unmatched</span>
      <span>{{ (match_result.unmatched * 100).toFixed(2) }}%</span>
    </div>
    <div class="item" v-for="person of match_result.top">
      <span>{{ person.name }}</span>
      <span>{{ (person.sim * 100).toFixed(2) }}%</span>
    </div>
  </div>
</template>

<style>
.item {
  display: flex;
  width: 50vw;
  justify-content: space-between;
  margin-bottom: 10px;
}
</style>
