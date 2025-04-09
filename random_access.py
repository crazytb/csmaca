import numpy as np
import random
import csv

# 시뮬레이션 파라미터
SIM_TIME = 100000              # 총 시뮬레이션 시간 (μs)
SLOT_TIME = 9                  # 슬롯 단위 시간
DIFS = 34                  # DIFS 시간
NUM_STAS = 5                   # STA 수
CW_MIN = 15
CW_MAX = 1023
PPDU_DURATION_RANGE = (50//9, 500//9)
# NPCA_THRESHOLD = 80
SWITCHING_DELAY = 10    # 슬롯
# PRIMARY_OCCUPANCY_PROB = 0.3

class STA:
    def __init__(self, id, use_npca=False):
        self.id = id
        self.use_npca = use_npca
        self.cw = CW_MIN
        self.state = "idle" # "idle", "backoff", "transmitting", "on_difs"
        self.backoff = 0
        self.remaining_difs = 0
        self.remaining_tx = 0
        self.ppdu_duration = 0
        self.current_channel = "primary"  # 'primary' 또는 'npca'
        self.primary_channel = None
        self.npca_channel = None
        self.last_packet_time = 0
        
    def set_channel(self, channel):
        # Channel: 1 or 2
        assert channel in [1, 2], "Invalid channel number"
        self.primary_channel = channel
        self.npca_channel = 3-channel
        
    def generate_ppdu(self, current_time):
        # PPDU 생성 로직
        self.ppdu_duration = np.random.randint(*PPDU_DURATION_RANGE)
        self.remaining_tx = self.ppdu_duration
        self.backoff = np.random.randint(0, self.cw + 1)
        self.remaining_difs = DIFS // SLOT_TIME
        self.state = "on_difs"
        self.last_packet_time = current_time
        
    def reset_backoff(self, current_time, collision=False):
        if collision:
            self.cw = min((self.cw + 1) * 2 - 1, CW_MAX)
        else:
            self.cw = CW_MIN
        self.backoff = np.random.randint(0, self.cw + 1)
        self.ppdu_duration = 0
        self.current_channel = "primary"
        
    
        
    
        
        
    def begin_transmission(self):
        assert self.state == "on_difs", "STA is not in DIFS state"
        assert self.remaining_tx == 0, "STA has remaining transmission time"
        if self.use_npca and self.in_npca:
        
            self.state = "transmitting"
            self.remaining_tx = self.ppdu_duration
            self.last_aoi = self.packet_arrival_time + self.ppdu_duration
        

class Channel:
    def __init__(self):
        self.state = ["idle"] * 2
        

def random_access(npca=False):
    stas = [STA(i, use_npca=npca) for i in range(NUM_STAS)]
    for i, sta in enumerate(stas):
        sta.set_channel(1) if i < NUM_STAS // 2 else sta.set_channel(2)
    
    channel = Channel()
    current_time = 0
    logs = []
    
    while current_time < SIM_TIME:
        transmitting_stas = []
        
        # 모든 STA의 상태를 확인
        for sta in stas:
            if sta.remaining_tx > 0:
                sta.remaining_tx -= 1
                if sta.remaining_tx == 0:
                    sta.state = "idle"
                continue
    

if __name__ == "__main__":
    dflog = random_access(npca=False)
