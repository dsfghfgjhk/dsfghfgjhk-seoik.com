/* Home-screen installation and offline study. No account data is cached here. */
(() => {
  "use strict";
  // The native iOS wrapper already is an app; do not offer web installation.
  if (window.__SEOIK_NATIVE_APP__ === true) return;
  const myView = document.querySelector('[data-view="my"]');
  if (!myView) return;

  const panel = document.createElement("section");
  panel.className = "pwa-install";
  panel.setAttribute("aria-labelledby", "pwa-title");
  panel.innerHTML = `
    <h2 id="pwa-title">홈 화면에 앱 설치</h2>
    <p>아이폰과 안드로이드에서 서익닷컴을 앱처럼 열 수 있어요.</p>
    <button type="button" id="pwa-install-button" hidden>앱 설치하기</button>
    <details>
      <summary>아이폰·아이패드 설치 방법</summary>
      <ol>
        <li>Safari에서 이 사이트를 열어요.</li>
        <li>공유 버튼을 누르고 <b>홈 화면에 추가</b>를 선택해요.</li>
        <li><b>웹 앱으로 열기</b>가 표시되면 켠 뒤 <b>추가</b>를 눌러요.</li>
      </ol>
    </details>
    <details>
      <summary>안드로이드 설치 방법</summary>
      <p>Chrome에서 <b>앱 설치하기</b>를 누르거나, 브라우저 메뉴의 <b>앱 설치</b> 또는 <b>홈 화면에 추가</b>를 선택해요.</p>
    </details>
    <p class="pwa-status" id="pwa-status" role="status">오프라인 학습을 준비하고 있어요.</p>
    <p class="pwa-status">오프라인에서도 문제와 개념노트를 볼 수 있어요. 로그인과 클라우드 동기화는 인터넷 연결이 필요해요.</p>`;
  const anchor = myView.querySelector("#accCard") || myView.querySelector(".topbar");
  if (anchor) anchor.after(panel);
  else myView.append(panel);

  const standalone = window.matchMedia("(display-mode: standalone)");
  const updateVisibility = () => {
    // Safari also exposes navigator.standalone for home-screen web apps.
    panel.hidden = standalone.matches || window.navigator.standalone === true;
  };
  updateVisibility();
  standalone.addEventListener("change", updateVisibility);

  const button = panel.querySelector("button");
  const status = panel.querySelector("#pwa-status");
  let installPrompt;
  window.addEventListener("beforeinstallprompt", event => {
    event.preventDefault();
    installPrompt = event;
    button.hidden = false;
  });
  button.addEventListener("click", async () => {
    if (!installPrompt) return;
    const prompt = installPrompt;
    installPrompt = null;
    button.hidden = true;
    try {
      await prompt.prompt();
      await prompt.userChoice;
    } catch {
      status.textContent = "브라우저 메뉴에서 홈 화면에 추가를 선택해 주세요.";
    }
  });
  window.addEventListener("appinstalled", () => {
    installPrompt = null;
    button.hidden = true;
    panel.hidden = true;
  });

  if (!("serviceWorker" in navigator) || !window.isSecureContext) {
    status.textContent = "홈 화면 설치와 오프라인 학습은 HTTPS 주소에서 사용할 수 있어요.";
    return;
  }
  // Check for a new worker on launch and when the app returns to the foreground.
  const hadController = !!navigator.serviceWorker.controller;
  const startedAt = Date.now();
  let reloaded = false;
  navigator.serviceWorker.addEventListener("controllerchange", () => {
    // Refresh only on the home screen shortly after launch, never during a quiz or editing.
    if (hadController && !reloaded && Date.now() - startedAt < 15000 &&
        document.visibilityState === "visible" && document.body.classList.contains("view-home")) {
      reloaded = true;
      window.location.reload();
    }
  });
  // A relative URL supports both a custom domain and GitHub Pages subdirectories.
  navigator.serviceWorker.register("./sw.js", { updateViaCache: "none" }).then(async registration => {
    let lastCheck = 0;
    const checkUpdate = () => {
      if (Date.now() - lastCheck < 60000) return;
      lastCheck = Date.now();
      registration.update().catch(() => {});
    };
    checkUpdate();
    document.addEventListener("visibilitychange", () => {
      if (document.visibilityState === "visible") checkUpdate();
    });
    const worker = registration.installing;
    if (!registration.active && worker) {
      await new Promise((resolve, reject) => {
        const check = () => {
          if (worker.state === "activated") {
            worker.removeEventListener("statechange", check);
            resolve();
          } else if (worker.state === "redundant") {
            worker.removeEventListener("statechange", check);
            reject(new Error("Offline installation failed"));
          }
        };
        worker.addEventListener("statechange", check);
        check();
      });
    }
    await navigator.serviceWorker.ready;
    status.textContent = "오프라인 학습 준비가 끝났어요.";
  }).catch(() => {
    status.textContent = "오프라인 저장을 완료하지 못했어요. 인터넷에 연결한 뒤 다시 열어 주세요.";
  });
})();
