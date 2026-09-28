"use client";

import { useState } from "react";

type Coordinates = {
  latitude: number;
  longitude: number;
  accuracy: number;
};

// Geolocation 오류 코드를 사용자에게 보여줄 문구로 변환
function describeGeolocationError(error: GeolocationPositionError): string {
  switch (error.code) {
    case error.PERMISSION_DENIED:
      return "위치 권한이 거부되었습니다. 브라우저 설정에서 위치 접근을 허용해 주세요.";
    case error.POSITION_UNAVAILABLE:
      return "현재 위치를 확인할 수 없습니다.";
    case error.TIMEOUT:
      return "위치 확인 시간이 초과되었습니다. 다시 시도해 주세요.";
    default:
      return "위치를 가져오는 중 오류가 발생했습니다.";
  }
}

function getCurrentPosition(): Promise<GeolocationPosition> {
  return new Promise((resolve, reject) =>
    navigator.geolocation.getCurrentPosition(resolve, reject, {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0,
    }),
  );
}

async function saveLocation(coords: Coordinates): Promise<void> {
  const response = await fetch("/api/locations", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(coords),
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
}

export default function HomePage() {
  const [coords, setCoords] = useState<Coordinates | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [saveStatus, setSaveStatus] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleClick = async () => {
    if (!("geolocation" in navigator)) {
      setErrorMessage("이 브라우저는 위치 정보를 지원하지 않습니다.");
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);
    setSaveStatus(null);

    let current: Coordinates;
    try {
      const position = await getCurrentPosition();
      current = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        accuracy: position.coords.accuracy,
      };
      setCoords(current);
    } catch (error) {
      setCoords(null);
      setErrorMessage(describeGeolocationError(error as GeolocationPositionError));
      setIsLoading(false);
      return;
    }

    // 위치 표시는 저장 성공 여부와 관계없이 유지
    try {
      await saveLocation(current);
      setSaveStatus("서버에 저장되었습니다.");
    } catch {
      setSaveStatus("서버 저장에 실패했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main>
      <div className="location-text" aria-live="polite">
        {isLoading && !coords && "위치를 확인하는 중..."}
        {errorMessage && <span className="error">{errorMessage}</span>}
        {coords && (
          <>
            {`위도: ${coords.latitude.toFixed(6)}\n경도: ${coords.longitude.toFixed(6)}\n정확도: ±${Math.round(coords.accuracy)}m`}
            {saveStatus && <div className="save-status">{saveStatus}</div>}
          </>
        )}
      </div>
      <button className="gps-button" onClick={handleClick} disabled={isLoading}>
        GPS
      </button>
    </main>
  );
}
