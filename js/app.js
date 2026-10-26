/**
 * TAMIYA MINI 4WD ITALIA - APPLICATION LOGIC & CONFIGURATOR ENGINE
 */

document.addEventListener("DOMContentLoaded", () => {
  // =========================================================================
  // APPLICATION STATE
  // =========================================================================
  const state = {
    currentCategory: "bmax", // Default to B-Max GP
    selectedPartIds: new Set(),
    currentTypeFilter: "all",
    legalOnlyFilter: true,
    searchQuery: "",
    lightbox: {
      part: null,
      currentImgIndex: 0,
      zoomLevel: 1.0,
      panX: 0,
      panY: 0,
      isDragging: false,
      startX: 0,
      startY: 0
    }
  };

  // Fallback SVG image for components if remote CDN image is offline
  const FALLBACK_IMAGE = "data:image/svg+xml;charset=UTF-8,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22300%22%20height%3D%22200%22%20viewBox%3D%220%200%20300%20200%22%3E%3Crect%20fill%3D%22%2318202e%22%20width%3D%22300%22%20height%3D%22200%22%2F%3E%3Ctext%20fill%3D%22%2300d2ff%22%20font-family%3D%22sans-serif%22%20font-size%3D%2214%22%20font-weight%3D%22bold%22%20x%3D%2250%25%22%20y%3D%2245%25%22%20text-anchor%3D%22middle%22%3ETAMIYA%20MINI%204WD%3C%2Ftext%3E%3Ctext%20fill%3D%22%2394a3b8%22%20font-family%3D%22sans-serif%22%20font-size%3D%2211%22%20x%3D%2250%25%22%20y%3D%2260%25%22%20text-anchor%3D%22middle%22%3EOfficial%20Tune-Up%20Part%3C%2Ftext%3E%3C%2Fsvg%3E";

  // Clean up any old localStorage override from previous versions
  try {
    localStorage.removeItem("tamiya_custom_db");
  } catch (e) {
    // ignore
  }

  // Official Data Store directly from js/data.js (maintained via Python scripts)
  const componentsData = TAMIYA_COMPONENTS;
  const categoriesData = MINI4WD_CATEGORIES;

  // Bootstrap Modals & Toasts instances
  const lightboxModalEl = document.getElementById("lightboxModal");
  const techDetailsModalEl = document.getElementById("techDetailsModal");
  const appToastEl = document.getElementById("appToast");

  const lightboxModal = new bootstrap.Modal(lightboxModalEl);
  const techDetailsModal = new bootstrap.Modal(techDetailsModalEl);
  const appToast = new bootstrap.Toast(appToastEl, { delay: 3500 });

  // =========================================================================
  // TOAST NOTIFICATION HELPER
  // =========================================================================
  function showToast(message, iconClass = "bi-info-circle-fill", textClass = "text-info") {
    const toastIcon = document.getElementById("toastIcon");
    const toastMsg = document.getElementById("toastMessage");
    toastIcon.className = `bi ${iconClass} ${textClass} fs-5`;
    toastMsg.textContent = message;
    appToast.show();
  }

  // =========================================================================
  // CATEGORY SWITCHER & RENDERING
  // =========================================================================
  function renderCategoryCards() {
    const container = document.getElementById("categoriesSection");
    if (!container) return;

    container.innerHTML = Object.values(categoriesData).map(cat => {
      const isActive = cat.id === state.currentCategory;
      return `
        <div class="col-12 col-md-6 col-lg-4">
          <div class="category-card ${isActive ? 'active' : ''}" data-cat-id="${cat.id}" style="--cat-color: ${cat.color};">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <span class="badge" style="background-color: ${cat.color}; font-size: 0.75rem;">
                <i class="bi ${cat.icon} me-1"></i> ${cat.badge}
              </span>
              <span class="badge bg-dark border border-secondary text-muted" style="font-size: 0.7rem;">
                ${cat.difficulty}
              </span>
            </div>
            <h5 class="fw-bold text-white mb-1 font-heading">${cat.name}</h5>
            <p class="text-muted small mb-2 text-truncate-2" style="font-size: 0.85rem;">
              ${cat.tagline}
            </p>
            <div class="d-flex justify-content-between align-items-center pt-2 border-top border-secondary border-opacity-25 small">
              <span class="text-muted"><i class="bi bi-speedometer2 text-warning me-1"></i> ${cat.speedIndex}</span>
              <span class="fw-bold ${isActive ? 'text-info' : 'text-primary'}">
                ${isActive ? '<i class="bi bi-check-circle-fill me-1"></i> Selezionata' : 'Esplora &rarr;'}
              </span>
            </div>
          </div>
        </div>
      `;
    }).join("");

    // Add click listeners to category cards
    container.querySelectorAll(".category-card").forEach(card => {
      card.addEventListener("click", () => {
        const catId = card.getAttribute("data-cat-id");
        setCategory(catId);
      });
    });
  }

  function setCategory(catId) {
    if (!categoriesData[catId]) return;
    state.currentCategory = catId;

    // Sync navbar selector
    const navSelect = document.getElementById("navbarCategorySelect");
    if (navSelect && navSelect.value !== catId) {
      navSelect.value = catId;
    }

    // Update UI components
    renderCategoryCards();
    renderCategoryGuide();
    renderPaddockTips();
    renderComponentsGrid();
    updateSummaryAndLegality();

    const cat = categoriesData[catId];
    showToast(`Categoria attivata: ${cat.name}. Componenti legali precaricati!`, "bi-check-circle-fill", "text-success");
  }

  // =========================================================================
  // CATEGORY DEEP DIVE GUIDE RENDERER
  // =========================================================================
  function renderCategoryGuide() {
    const container = document.getElementById("categoryGuideContainer");
    if (!container) return;

    const cat = categoriesData[state.currentCategory];
    if (!cat) return;

    // Update labels
    const builderLabel = document.getElementById("builderCategoryLabel");
    if (builderLabel) builderLabel.textContent = cat.name;

    const summaryBadge = document.getElementById("summaryCategoryBadge");
    if (summaryBadge) summaryBadge.textContent = cat.badge;

    container.innerHTML = `
      <div class="guide-card">
        <!-- Header Banner -->
        <div class="d-flex flex-column flex-lg-row justify-content-between align-items-lg-center gap-3 pb-4 mb-4 border-bottom border-secondary border-opacity-50">
          <div>
            <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
              <span class="badge px-3 py-1 font-heading" style="background-color: ${cat.color}; font-size: 0.85rem;">
                <i class="bi ${cat.icon} me-1"></i> ${cat.badge}
              </span>
              <span class="spec-badge-pill"><i class="bi bi-wallet2 text-success"></i> Costo: ${cat.costIndex}</span>
              <span class="spec-badge-pill"><i class="bi bi-flag-fill text-warning"></i> Livello: ${cat.difficulty}</span>
            </div>
            <h2 class="display-6 fw-bold text-white mb-1 font-heading">${cat.name}</h2>
            <p class="text-info mb-0 fw-semibold fs-5">${cat.tagline}</p>
          </div>

          <!-- Quick Action: Load Recommended Build -->
          <div class="d-flex flex-column gap-2 mt-2 mt-lg-0">
            <button class="btn btn-outline-info d-flex align-items-center justify-content-center gap-2 py-2 w-100 w-lg-auto" id="btnLoadPreset">
              <i class="bi bi-magic"></i>
              <span>Carica Setup Consigliato Vincitore</span>
            </button>
            <span class="text-muted small text-center text-lg-end">Preset 100% conforme di scatola</span>
          </div>
        </div>

        <!-- Philosophy & Track Context -->
        <div class="mb-4">
          <h5 class="text-uppercase text-white fw-bold mb-2 font-heading"><i class="bi bi-info-circle text-primary me-2"></i>Filosofia & Caratteristiche della Categoria</h5>
          <div class="p-3 rounded bg-dark border border-secondary border-opacity-50 text-white leading-relaxed">
            ${cat.description}
            <div class="mt-2 pt-2 border-top border-secondary border-opacity-25 small text-muted">
              <strong class="text-info"><i class="bi bi-geo-alt-fill me-1"></i>Tipo di Tracciato Tipico:</strong> ${cat.trackType}
            </div>
          </div>
        </div>

        <!-- Rules Columns: What is Allowed vs What is Forbidden -->
        <div class="row g-3 g-md-4 mb-4">
          <!-- Allowed Column -->
          <div class="col-12 col-lg-6">
            <div class="rule-box-allowed h-100">
              <h5 class="text-success fw-bold font-heading mb-3 d-flex align-items-center gap-2" style="font-size: 0.95rem;">
                <i class="bi bi-check-circle-fill"></i> COSA SI PUÒ FARE / MONTARE (CONSENTITO)
              </h5>
              <ul class="list-unstyled mb-0 d-flex flex-column gap-2">
                ${cat.rulesAllowed.map(rule => `
                  <li class="d-flex align-items-start gap-2 small text-white">
                    <i class="bi bi-check2 text-success fs-6 mt-1 flex-shrink-0"></i>
                    <span>${rule}</span>
                  </li>
                `).join("")}
              </ul>
            </div>
          </div>

          <!-- Forbidden Column -->
          <div class="col-12 col-lg-6">
            <div class="rule-box-forbidden h-100">
              <h5 class="text-danger fw-bold font-heading mb-3 d-flex align-items-center gap-2" style="font-size: 0.95rem;">
                <i class="bi bi-x-octagon-fill"></i> COSA È VIETATO (SQUALIFICA IN VERIFICA)
              </h5>
              <ul class="list-unstyled mb-0 d-flex flex-column gap-2">
                ${cat.rulesForbidden.map(rule => `
                  <li class="d-flex align-items-start gap-2 small text-white">
                    <i class="bi bi-exclamation-triangle-fill text-danger fs-6 mt-1 flex-shrink-0"></i>
                    <span>${rule}</span>
                  </li>
                `).join("")}
              </ul>
            </div>
          </div>
        </div>

        <!-- Dimensions & Technical Scrutineering Box -->
        <div class="mb-4">
          <h5 class="text-uppercase text-white fw-bold mb-3 font-heading"><i class="bi bi-rulers text-warning me-2"></i>Dima Tecnica & Limiti Dimensionali Ufficiali</h5>
          <div class="row g-2 text-center">
            <div class="col-6 col-md-3">
              <div class="p-2 p-md-3 rounded bg-dark border border-secondary border-opacity-50 text-center h-100 d-flex flex-column justify-content-center">
                <div class="text-muted dimension-label">Larghezza Max</div>
                <div class="fw-bold text-white fs-6 font-heading mt-1">${cat.dimensions.maxWidth}</div>
              </div>
            </div>
            <div class="col-6 col-md-3">
              <div class="p-2 p-md-3 rounded bg-dark border border-secondary border-opacity-50 text-center h-100 d-flex flex-column justify-content-center">
                <div class="text-muted dimension-label">Lunghezza Max</div>
                <div class="fw-bold text-white fs-6 font-heading mt-1">${cat.dimensions.maxLength}</div>
              </div>
            </div>
            <div class="col-6 col-md-3">
              <div class="p-2 p-md-3 rounded bg-dark border border-secondary border-opacity-50 text-center h-100 d-flex flex-column justify-content-center">
                <div class="text-muted dimension-label">Luce da Terra Minima</div>
                <div class="fw-bold text-warning fs-6 font-heading mt-1">${cat.dimensions.minGroundClearance}</div>
              </div>
            </div>
            <div class="col-6 col-md-3">
              <div class="p-2 p-md-3 rounded bg-dark border border-secondary border-opacity-50 text-center h-100 d-flex flex-column justify-content-center">
                <div class="text-muted dimension-label">Peso Minimo (in marcia)</div>
                <div class="fw-bold text-success fs-6 font-heading mt-1">${cat.dimensions.minWeight}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pro-Tips from Italian Paddock -->
        <div class="p-3 rounded bg-dark border-start border-4 border-info">
          <div class="d-flex align-items-start gap-2">
            <i class="bi bi-lightbulb-fill text-info fs-5 mt-1 flex-shrink-0"></i>
            <div>
              <strong class="text-white font-heading d-block">CONSIGLIO DELL'ESPERTO PER L'ASSETTO IN ITALIA</strong>
              <p class="text-muted small mb-0">${cat.setupTips}</p>
            </div>
          </div>
        </div>

      </div>
    `;

    // Hook preset button
    const btnLoad = container.querySelector("#btnLoadPreset");
    if (btnLoad) {
      btnLoad.addEventListener("click", () => loadPreset(state.currentCategory));
    }
  }

  // =========================================================================
  // PADDOCK TECH & ADVANCED SETUP TIPS RENDERER
  // =========================================================================
  function renderPaddockTips() {
    const container = document.getElementById("paddockTipsContainer");
    const labelEl = document.getElementById("paddockCategoryLabel");
    if (!container) return;

    const cat = categoriesData[state.currentCategory];
    if (labelEl && cat) {
      labelEl.textContent = cat.name;
    }

    const tips = (typeof CATEGORY_PADDOCK_TIPS !== "undefined" && CATEGORY_PADDOCK_TIPS[state.currentCategory]) || [];
    if (tips.length === 0) {
      container.innerHTML = `<div class="col-12 text-muted">Nessun consiglio specifico disponibile per questa categoria.</div>`;
      return;
    }

    container.innerHTML = tips.map(tip => `
      <div class="col-12 col-md-6 col-lg-3">
        <div class="paddock-tip-card">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <div class="paddock-tip-icon">
              <i class="bi ${tip.icon}"></i>
            </div>
            <span class="badge bg-dark border border-secondary border-opacity-50 text-warning" style="font-size: 0.7rem;">
              ${tip.badge}
            </span>
          </div>
          <h6 class="fw-bold text-white mb-2 font-heading" style="font-size: 0.95rem; line-height: 1.35;">
            ${tip.title}
          </h6>
          <p class="text-info small fw-semibold mb-2" style="font-size: 0.8rem;">
            ${tip.summary}
          </p>
          <p class="text-muted small mb-0 flex-grow-1" style="font-size: 0.82rem; line-height: 1.5;">
            ${tip.content}
          </p>
        </div>
      </div>
    `).join("");
  }

  // =========================================
  // COMPONENT CARDS & GRID RENDERING
  // =========================================
  function renderComponentsGrid() {
    const grid = document.getElementById("componentsGrid");
    if (!grid) return;

    let items = componentsData;

    // Filter by Component Type Tab
    if (state.currentTypeFilter !== "all") {
      items = items.filter(it => it.category === state.currentTypeFilter);
    }

    // Filter by Legal Only toggle
    if (state.legalOnlyFilter) {
      items = items.filter(it => it.allowedCategories.includes(state.currentCategory));
    }

    // Filter by Search Query
    if (state.searchQuery.trim() !== "") {
      const q = state.searchQuery.toLowerCase().trim();
      items = items.filter(it => 
        it.itemNumber.toLowerCase().includes(q) ||
        it.name.toLowerCase().includes(q) ||
        it.description.toLowerCase().includes(q)
      );
    }

    if (items.length === 0) {
      grid.innerHTML = `
        <div class="col-12 text-center py-5">
          <div class="card bg-dark border-secondary border-opacity-50 p-5">
            <i class="bi bi-funnel text-muted fs-1 mb-3"></i>
            <h5 class="text-white">Nessun componente trovato</h5>
            <p class="text-muted small">Nessun articolo corrisponde ai filtri impostati. Prova a disattivare il filtro 'Solo Legali' o a cancellare la ricerca.</p>
            <button class="btn btn-sm btn-outline-info mx-auto" style="width: auto;" id="btnResetFilters">
              Mostra Tutti i Componenti
            </button>
          </div>
        </div>
      `;
      const btnReset = grid.querySelector("#btnResetFilters");
      if (btnReset) {
        btnReset.addEventListener("click", () => {
          state.currentTypeFilter = "all";
          state.legalOnlyFilter = false;
          state.searchQuery = "";
          const legalToggle = document.getElementById("legalOnlyToggle");
          if (legalToggle) legalToggle.checked = false;
          const searchInput = document.getElementById("componentSearchInput");
          if (searchInput) searchInput.value = "";
          updateFilterPills();
          renderComponentsGrid();
        });
      }
      return;
    }

    grid.innerHTML = items.map(item => {
      const isInBuild = state.selectedPartIds.has(item.id);
      const isLegal = item.allowedCategories.includes(state.currentCategory);
      const ruleNote = item.rulesNotes?.[state.currentCategory] || (isLegal ? "Componente ammesso dal regolamento ufficiale." : "Componente non omologato per questa categoria.");
      
      // Spec highlights
      const firstSpecs = Object.entries(item.specs).slice(0, 3);

      return `
        <div class="col-12 col-md-6 col-lg-4 col-xl-3">
          <div class="part-card ${isInBuild ? 'in-build' : ''}" data-part-id="${item.id}">
            
            <!-- Image Wrapper with Carousel & Zoom Trigger -->
            <div class="part-img-wrapper" id="imgWrap_${item.id}">
              <img src="${item.images[0]}" alt="${item.name}" id="img_${item.id}" onerror="this.onerror=null; this.src=(window.FALLBACK_IMG || '${FALLBACK_IMAGE}');">
              
              <!-- Zoom Lightbox Button -->
              <button class="img-zoom-btn" title="Ingrandisci immagine" data-action="zoom" data-part-id="${item.id}">
                <i class="bi bi-zoom-in"></i>
              </button>

              ${item.images.length > 1 ? `
                <button class="img-nav-btn prev" data-action="prev-img" data-part-id="${item.id}"><i class="bi bi-chevron-left"></i></button>
                <button class="img-nav-btn next" data-action="next-img" data-part-id="${item.id}"><i class="bi bi-chevron-right"></i></button>
              ` : ''}

              <!-- Image count indicator -->
              ${item.images.length > 1 ? `
                <div class="position-absolute bottom-0 start-50 translate-middle-x pb-1">
                  <span class="badge bg-dark bg-opacity-75 text-white" style="font-size: 0.65rem;" id="badgeCount_${item.id}">
                    1 / ${item.images.length}
                  </span>
                </div>
              ` : ''}
            </div>

            <!-- Card Body -->
            <div class="p-3 d-flex flex-column flex-grow-1 justify-content-between">
              <div>
                <!-- Item Code & Price -->
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <span class="item-tag">Item #${item.itemNumber}</span>
                  <span class="fw-bold text-success fs-6">€ ${item.price.toFixed(2)}</span>
                </div>

                <!-- Product Name -->
                <h6 class="fw-bold text-white mb-2" style="font-size: 0.95rem; line-height: 1.35;">
                  ${item.name}
                </h6>

                <!-- Legality Status Badge -->
                <div class="mb-2">
                  ${isLegal ? `
                    <span class="badge bg-success bg-opacity-25 text-success border border-success border-opacity-50" style="font-size: 0.72rem;">
                      <i class="bi bi-check-circle-fill me-1"></i> 100% Legale in ${categoriesData[state.currentCategory].badge}
                    </span>
                  ` : `
                    <span class="badge bg-danger bg-opacity-25 text-danger border border-danger border-opacity-50" style="font-size: 0.72rem;">
                      <i class="bi bi-slash-circle-fill me-1"></i> VIETATO in ${categoriesData[state.currentCategory].badge}
                    </span>
                  `}
                </div>

                <!-- Brief Specs Snippet -->
                <div class="bg-dark rounded p-2 border border-secondary border-opacity-25 mb-3" style="font-size: 0.78rem;">
                  ${firstSpecs.map(([k, v]) => `
                    <div class="d-flex justify-content-between text-muted text-truncate">
                      <span>${k}:</span>
                      <strong class="text-white text-truncate ms-2">${v}</strong>
                    </div>
                  `).join("")}
                </div>
              </div>

              <!-- Action Buttons -->
              <div>
                <div class="d-flex gap-2 mb-2">
                  <button class="btn btn-sm btn-outline-secondary w-50 py-2 d-flex align-items-center justify-content-center" data-action="details" data-part-id="${item.id}">
                    <i class="bi bi-info-circle me-1"></i> Dettagli
                  </button>
                  <a href="${item.tamiyaUrl}" target="_blank" class="btn btn-sm btn-outline-primary w-50 py-2 d-flex align-items-center justify-content-center" title="Apri pagina ufficiale Tamiya">
                    <i class="bi bi-box-arrow-up-right me-1"></i> Tamiya
                  </a>
                </div>

                <button class="btn btn-sm w-100 fw-bold py-2 d-flex align-items-center justify-content-center ${isInBuild ? 'btn-danger' : (isLegal ? 'btn-primary' : 'btn-outline-danger')}" data-action="toggle-build" data-part-id="${item.id}">
                  ${isInBuild ? '<i class="bi bi-dash-circle me-1"></i> Rimuovi dal Build' : '<i class="bi bi-plus-circle me-1"></i> Aggiungi al Build'}
                </button>
              </div>

            </div>

          </div>
        </div>
      `;
    }).join("");

    attachCardEventListeners();
  }

  function attachCardEventListeners() {
    const grid = document.getElementById("componentsGrid");
    if (!grid) return;

    // Carousel Image Switching per card
    grid.querySelectorAll("[data-action='next-img']").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const partId = btn.getAttribute("data-part-id");
        switchCardImage(partId, 1);
      });
    });

    grid.querySelectorAll("[data-action='prev-img']").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const partId = btn.getAttribute("data-part-id");
        switchCardImage(partId, -1);
      });
    });

    // Touch swipe support on card images
    grid.querySelectorAll(".part-img-wrapper").forEach(wrapper => {
      let touchStartX = 0;
      let touchEndX = 0;

      wrapper.addEventListener("touchstart", (e) => {
        touchStartX = e.changedTouches[0].screenX;
      }, { passive: true });

      wrapper.addEventListener("touchend", (e) => {
        touchEndX = e.changedTouches[0].screenX;
        const partId = wrapper.id.replace("imgWrap_", "");
        const diff = touchEndX - touchStartX;
        if (Math.abs(diff) > 40) {
          if (diff < 0) {
            switchCardImage(partId, 1);
          } else {
            switchCardImage(partId, -1);
          }
        }
      }, { passive: true });
    });

    // Zoom Lightbox Modal
    grid.querySelectorAll("[data-action='zoom']").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const partId = btn.getAttribute("data-part-id");
        openLightbox(partId);
      });
    });

    // Technical Details Modal
    grid.querySelectorAll("[data-action='details']").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const partId = btn.getAttribute("data-part-id");
        openTechDetails(partId);
      });
    });

    // Toggle Part In Build
    grid.querySelectorAll("[data-action='toggle-build']").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const partId = btn.getAttribute("data-part-id");
        togglePartInBuild(partId);
      });
    });
  }

  // Helper to cycle images inside the card
  const cardImageIndexes = {};
  function switchCardImage(partId, delta) {
    const part = componentsData.find(p => p.id === partId);
    if (!part || part.images.length <= 1) return;

    if (!cardImageIndexes[partId]) cardImageIndexes[partId] = 0;
    cardImageIndexes[partId] = (cardImageIndexes[partId] + delta + part.images.length) % part.images.length;

    const imgEl = document.getElementById(`img_${partId}`);
    const badgeEl = document.getElementById(`badgeCount_${partId}`);
    if (imgEl) {
      imgEl.src = part.images[cardImageIndexes[partId]];
    }
    if (badgeEl) {
      badgeEl.textContent = `${cardImageIndexes[partId] + 1} / ${part.images.length}`;
    }
  }

  // =========================================================================
  // BUILD SELECTION & LEGALITY ENGINE
  // =========================================================================
  function togglePartInBuild(partId) {
    const part = componentsData.find(p => p.id === partId);
    if (!part) return;

    if (state.selectedPartIds.has(partId)) {
      state.selectedPartIds.delete(partId);
      showToast(`Rimosso: ${part.name}`, "bi-dash-circle", "text-warning");
    } else {
      // If adding a chassis and one is already selected, notify user
      if (part.category === "chassis") {
        const existingChassis = Array.from(state.selectedPartIds).find(id => {
          const p = componentsData.find(x => x.id === id);
          return p && p.category === "chassis";
        });
        if (existingChassis) {
          state.selectedPartIds.delete(existingChassis);
        }
      }

      state.selectedPartIds.add(partId);
      showToast(`Aggiunto al Build: ${part.name}`, "bi-plus-circle", "text-success");
    }

    renderComponentsGrid();
    updateSummaryAndLegality();
  }

  function loadPreset(categoryId) {
    const preset = RECOMMENDED_BUILDS[categoryId];
    if (!preset) return;

    state.selectedPartIds = new Set(preset.parts);
    renderComponentsGrid();
    updateSummaryAndLegality();
    showToast(`Caricato setup vincente: ${preset.name}!`, "bi-magic", "text-success");
  }

  // =========================================================================
  // LIVE LEGALITY CHECKER & BOM SUMMARY
  // =========================================================================
  function updateSummaryAndLegality() {
    const selectedParts = Array.from(state.selectedPartIds).map(id => componentsData.find(p => p.id === id)).filter(Boolean);
    
    // Total count & price
    const totalCount = selectedParts.length;
    const totalPrice = selectedParts.reduce((sum, p) => sum + p.price, 0);

    // Update counter in Navbar
    const navBuildCount = document.getElementById("navBuildCount");
    if (navBuildCount) navBuildCount.textContent = totalCount;

    // Update floating mobile dock
    const floatingBadge = document.getElementById("floatingCategoryBadge");
    const floatingBuild = document.getElementById("floatingBuildSummary");
    const floatingPrice = document.getElementById("floatingPriceSummary");
    if (floatingBadge && cat) floatingBadge.textContent = cat.badge;
    if (floatingBuild) floatingBuild.textContent = `${totalCount} ${totalCount === 1 ? 'Parte' : 'Parti'}`;
    if (floatingPrice) floatingPrice.textContent = `€ ${totalPrice.toFixed(2)}`;

    const summaryPartsCount = document.getElementById("summaryPartsCount");
    if (summaryPartsCount) summaryPartsCount.textContent = totalCount;

    const summaryTotalPrice = document.getElementById("summaryTotalPrice");
    if (summaryTotalPrice) summaryTotalPrice.textContent = `€ ${totalPrice.toFixed(2)}`;

    // Chassis detection
    const chassisPart = selectedParts.find(p => p.category === "chassis");
    const summaryChassisName = document.getElementById("summaryChassisName");
    if (summaryChassisName) {
      summaryChassisName.textContent = chassisPart ? chassisPart.name : "Nessuno";
    }

    // ===================================
    // LEGALITY & COMPATIBILITY CHECKS
    // ===================================
    const issues = [];

    // Check 1: Any part illegal for this category?
    const illegalParts = selectedParts.filter(p => !p.allowedCategories.includes(state.currentCategory));
    if (illegalParts.length > 0) {
      issues.push(`${illegalParts.length} componente/i VIETATO/I in ${cat.badge}: ${illegalParts.map(p => p.name).join(", ")}.`);
    }

    // Check 2: Motor vs Chassis shaft compatibility
    const motorPart = selectedParts.find(p => p.category === "motor");
    if (chassisPart && motorPart) {
      if (chassisPart.chassisType === "double" && motorPart.chassisType === "single") {
        issues.push(`Incompatibilità meccanica: Il telaio ${chassisPart.name} richiede motore PRO a doppio albero (Double Shaft). Il motore selezionato (${motorPart.name}) è a singolo albero!`);
      } else if (chassisPart.chassisType === "single" && motorPart.chassisType === "double") {
        issues.push(`Incompatibilità meccanica: Il telaio ${chassisPart.name} richiede motore standard a singolo albero. Il motore selezionato (${motorPart.name}) è un motore PRO a doppio albero!`);
      }
    }

    // Check 3: Tuned Class plate limit (Max 3 FRP/Carbon plates)
    if (state.currentCategory === "tuned") {
      const plateCount = selectedParts.filter(p => p.category === "plate").length;
      if (plateCount > 3) {
        issues.push(`Superato limite piastre per Tuned Class: Hai selezionato ${plateCount} piastre (il regolamento ne consente massimo 3 totali).`);
      }
    }

    // Check 4: Box Stock purity check
    if (state.currentCategory === "boxstock") {
      const tuneUpParts = selectedParts.filter(p => p.category !== "chassis");
      if (tuneUpParts.length > 0) {
        issues.push(`Violazione Box Stock: Nella classe scatola non puoi aggiungere parti Tune-Up opzionali.`);
      }
    }

    // Update Legality Badges & Banner
    const liveBanner = document.getElementById("liveLegalityBanner");
    const liveText = document.getElementById("liveLegalityText");
    const summaryLegalityScore = document.getElementById("summaryLegalityScore");

    if (issues.length === 0) {
      if (liveBanner) {
        liveBanner.className = "spec-badge-pill border-success text-success bg-dark p-2 px-3";
        liveBanner.querySelector("i").className = "bi bi-shield-check fs-5 text-success me-2 flex-shrink-0";
      }
      if (liveText) liveText.textContent = `100% Conforme al Regolamento ${cat.badge}`;
      if (summaryLegalityScore) {
        summaryLegalityScore.textContent = "100% Legale";
        summaryLegalityScore.className = "fs-5 fw-bold text-success";
      }
    } else {
      if (liveBanner) {
        liveBanner.className = "spec-badge-pill border-danger text-danger bg-dark p-2 px-3";
        liveBanner.querySelector("i").className = "bi bi-exclamation-octagon-fill fs-5 text-danger me-2 flex-shrink-0";
      }
      if (liveText) liveText.textContent = issues[0];
      if (summaryLegalityScore) {
        summaryLegalityScore.textContent = `${issues.length} Irregolarità`;
        summaryLegalityScore.className = "fs-5 fw-bold text-danger";
      }
    }

    // ===================================
    // RENDER BOM TABLE & MOBILE CARDS
    // ===================================
    const tableBody = document.getElementById("summaryTableBody");
    const emptyState = document.getElementById("summaryEmptyState");
    const partsTableWrapper = document.getElementById("summaryPartsTable")?.closest(".table-responsive");
    const mobileCards = document.getElementById("summaryMobileCards");

    if (selectedParts.length === 0) {
      if (tableBody) tableBody.innerHTML = "";
      if (mobileCards) mobileCards.innerHTML = "";
      if (emptyState) emptyState.style.display = "block";
      if (partsTableWrapper) partsTableWrapper.style.display = "none";
      if (mobileCards) mobileCards.style.display = "none";
      return;
    }

    if (emptyState) emptyState.style.display = "none";
    if (partsTableWrapper) partsTableWrapper.style.display = "";
    if (mobileCards) mobileCards.style.display = "";

    // 1. Render Desktop Table
    if (tableBody) {
      tableBody.innerHTML = selectedParts.map(part => {
        const isLegal = part.allowedCategories.includes(state.currentCategory);
        const ruleNote = part.rulesNotes?.[state.currentCategory] || (isLegal ? "Ammesso" : "Non omologato");

        return `
          <tr>
            <td>
              <div class="bg-white rounded p-1 text-center" style="width: 50px; height: 50px;">
                <img src="${part.images[0]}" alt="${part.name}" style="max-height: 100%; max-width: 100%; object-fit: contain;">
              </div>
            </td>
            <td>
              <span class="item-tag">#${part.itemNumber}</span>
            </td>
            <td>
              <div class="fw-bold text-white">${part.name}</div>
              <div class="small text-muted text-truncate" style="max-width: 320px;">${ruleNote}</div>
            </td>
            <td>
              <span class="badge bg-secondary text-uppercase" style="font-size: 0.7rem;">${part.category}</span>
            </td>
            <td>
              ${isLegal ? `
                <span class="badge bg-success bg-opacity-25 text-success border border-success border-opacity-50">
                  <i class="bi bi-check-circle-fill me-1"></i> Legale
                </span>
              ` : `
                <span class="badge bg-danger bg-opacity-25 text-danger border border-danger border-opacity-50">
                  <i class="bi bi-x-circle-fill me-1"></i> Vietato
                </span>
              `}
            </td>
            <td class="text-end fw-bold text-success">
              € ${part.price.toFixed(2)}
            </td>
            <td class="text-center no-print">
              <div class="btn-group btn-group-sm">
                <a href="${part.tamiyaUrl}" target="_blank" class="btn btn-outline-info" title="Scheda Ufficiale Tamiya.com">
                  <i class="bi bi-box-arrow-up-right"></i>
                </a>
                <a href="https://www.google.com/search?q=Tamiya+${part.itemNumber}+${encodeURIComponent(part.name)}" target="_blank" class="btn btn-outline-secondary" title="Trova negozi / Shop">
                  <i class="bi bi-cart"></i>
                </a>
              </div>
            </td>
            <td class="text-center no-print">
              <button class="btn btn-sm btn-outline-danger p-1" data-remove-id="${part.id}" title="Rimuovi">
                <i class="bi bi-trash"></i>
              </button>
            </td>
          </tr>
        `;
      }).join("");

      // Attach remove handlers
      tableBody.querySelectorAll("[data-remove-id]").forEach(btn => {
        btn.addEventListener("click", () => {
          const partId = btn.getAttribute("data-remove-id");
          togglePartInBuild(partId);
        });
      });
    }

    // 2. Render Mobile Cards
    if (mobileCards) {
      mobileCards.innerHTML = selectedParts.map(part => {
        const isLegal = part.allowedCategories.includes(state.currentCategory);

        return `
          <div class="summary-mobile-card">
            <div class="d-flex align-items-center gap-3">
              <div class="summary-mobile-thumb flex-shrink-0">
                <img src="${part.images[0]}" alt="${part.name}">
              </div>
              <div class="flex-grow-1 min-w-0">
                <div class="d-flex align-items-center justify-content-between gap-1 mb-1">
                  <span class="item-tag">#${part.itemNumber}</span>
                  <span class="fw-bold text-success fs-6">€ ${part.price.toFixed(2)}</span>
                </div>
                <div class="fw-bold text-white small text-truncate" title="${part.name}">${part.name}</div>
                <div class="d-flex flex-wrap align-items-center gap-1 mt-1">
                  <span class="badge bg-secondary text-uppercase" style="font-size: 0.65rem;">${part.category}</span>
                  ${isLegal ? `
                    <span class="badge bg-success bg-opacity-25 text-success border border-success border-opacity-50" style="font-size: 0.65rem;">
                      <i class="bi bi-check-circle-fill me-1"></i> Legale
                    </span>
                  ` : `
                    <span class="badge bg-danger bg-opacity-25 text-danger border border-danger border-opacity-50" style="font-size: 0.65rem;">
                      <i class="bi bi-x-circle-fill me-1"></i> Vietato
                    </span>
                  `}
                </div>
              </div>
            </div>
            <div class="d-flex align-items-center justify-content-between pt-2 mt-2 border-top border-secondary border-opacity-25 summary-mobile-actions gap-2">
              <div class="d-flex gap-2">
                <a href="${part.tamiyaUrl}" target="_blank" class="btn btn-sm btn-outline-info py-1 px-2" title="Scheda Ufficiale">
                  <i class="bi bi-box-arrow-up-right me-1"></i> Tamiya
                </a>
                <a href="https://www.google.com/search?q=Tamiya+${part.itemNumber}+${encodeURIComponent(part.name)}" target="_blank" class="btn btn-sm btn-outline-secondary py-1 px-2" title="Cerca Shop">
                  <i class="bi bi-cart me-1"></i> Shop
                </a>
              </div>
              <button class="btn btn-sm btn-outline-danger py-1 px-2" data-remove-id="${part.id}">
                <i class="bi bi-trash3 me-1"></i> Rimuovi
              </button>
            </div>
          </div>
        `;
      }).join("");

      // Attach remove handlers on mobile cards
      mobileCards.querySelectorAll("[data-remove-id]").forEach(btn => {
        btn.addEventListener("click", () => {
          const partId = btn.getAttribute("data-remove-id");
          togglePartInBuild(partId);
        });
      });
    }
  }

  // =========================================================================
  // LIGHTBOX / ZOOM IMAGE MODAL LOGIC
  // =========================================================================
  function openLightbox(partId) {
    const part = componentsData.find(p => p.id === partId);
    if (!part) return;

    state.lightbox.part = part;
    state.lightbox.currentImgIndex = 0;
    state.lightbox.zoomLevel = 1.0;
    state.lightbox.panX = 0;
    state.lightbox.panY = 0;

    document.getElementById("lightboxItemNumber").textContent = `Item #${part.itemNumber}`;
    document.getElementById("lightboxItemTitle").textContent = part.name;
    document.getElementById("lightboxTamiyaLink").href = part.tamiyaUrl;

    updateLightboxImage();
    renderLightboxThumbs();
    lightboxModal.show();
  }

  function updateLightboxImage() {
    const part = state.lightbox.part;
    if (!part) return;

    const imgEl = document.getElementById("lightboxImage");
    const indexEl = document.getElementById("lightboxImageIndex");

    imgEl.src = part.images[state.lightbox.currentImgIndex];
    imgEl.style.transform = `scale(${state.lightbox.zoomLevel}) translate(${state.lightbox.panX}px, ${state.lightbox.panY}px)`;
    indexEl.textContent = `Immagine ${state.lightbox.currentImgIndex + 1} di ${part.images.length}`;

    // Highlight active thumbnail
    document.querySelectorAll(".lightbox-thumb").forEach((th, idx) => {
      th.classList.toggle("border-primary", idx === state.lightbox.currentImgIndex);
      th.classList.toggle("border-secondary", idx !== state.lightbox.currentImgIndex);
    });
  }

  function renderLightboxThumbs() {
    const container = document.getElementById("lightboxThumbs");
    const part = state.lightbox.part;
    if (!container || !part) return;

    if (part.images.length <= 1) {
      container.innerHTML = "";
      return;
    }

    container.innerHTML = part.images.map((imgUrl, idx) => `
      <div class="lightbox-thumb rounded bg-white p-1 border ${idx === 0 ? 'border-primary' : 'border-secondary'}" data-thumb-idx="${idx}" style="cursor: pointer; width: 60px; height: 60px; display: inline-flex; align-items: center; justify-content: center;">
        <img src="${imgUrl}" alt="Thumb ${idx + 1}" style="max-height: 100%; max-width: 100%; object-fit: contain;">
      </div>
    `).join("");

    container.querySelectorAll(".lightbox-thumb").forEach(th => {
      th.addEventListener("click", () => {
        state.lightbox.currentImgIndex = parseInt(th.getAttribute("data-thumb-idx"), 10);
        state.lightbox.zoomLevel = 1.0;
        state.lightbox.panX = 0;
        state.lightbox.panY = 0;
        updateLightboxImage();
      });
    });
  }

  // Zoom Controls & Mouse Interactions
  document.getElementById("btnZoomIn")?.addEventListener("click", () => {
    state.lightbox.zoomLevel = Math.min(state.lightbox.zoomLevel + 0.3, 3.5);
    updateLightboxImage();
  });

  document.getElementById("btnZoomOut")?.addEventListener("click", () => {
    state.lightbox.zoomLevel = Math.max(state.lightbox.zoomLevel - 0.3, 0.7);
    updateLightboxImage();
  });

  document.getElementById("btnZoomReset")?.addEventListener("click", () => {
    state.lightbox.zoomLevel = 1.0;
    state.lightbox.panX = 0;
    state.lightbox.panY = 0;
    updateLightboxImage();
  });

  // Wheel zoom and pan drag support on lightbox image container
  const lightboxContainer = document.getElementById("lightboxContainer");
  if (lightboxContainer) {
    lightboxContainer.addEventListener("wheel", (e) => {
      e.preventDefault();
      const delta = e.deltaY < 0 ? 0.2 : -0.2;
      state.lightbox.zoomLevel = Math.max(0.7, Math.min(3.5, state.lightbox.zoomLevel + delta));
      updateLightboxImage();
    }, { passive: false });

    lightboxContainer.addEventListener("mousedown", (e) => {
      if (state.lightbox.zoomLevel > 1.0) {
        state.lightbox.isDragging = true;
        state.lightbox.startX = e.clientX - state.lightbox.panX;
        state.lightbox.startY = e.clientY - state.lightbox.panY;
      }
    });

    window.addEventListener("mousemove", (e) => {
      if (state.lightbox.isDragging) {
        state.lightbox.panX = e.clientX - state.lightbox.startX;
        state.lightbox.panY = e.clientY - state.lightbox.startY;
        const imgEl = document.getElementById("lightboxImage");
        if (imgEl) {
          imgEl.style.transform = `scale(${state.lightbox.zoomLevel}) translate(${state.lightbox.panX}px, ${state.lightbox.panY}px)`;
        }
      }
    });

    window.addEventListener("mouseup", () => {
      state.lightbox.isDragging = false;
    });
  }

  // =========================================================================
  // TECHNICAL SPECIFICATIONS MODAL LOGIC
  // =========================================================================
  function openTechDetails(partId) {
    const part = componentsData.find(p => p.id === partId);
    if (!part) return;

    document.getElementById("techModalItemNumber").textContent = `Item #${part.itemNumber}`;
    document.getElementById("techModalTitle").textContent = part.name;
    document.getElementById("techModalImage").src = part.images[0];
    document.getElementById("techModalDescription").textContent = part.description;
    document.getElementById("techModalChassis").textContent = `Tipo Telaio: ${part.chassisType.toUpperCase()}`;
    document.getElementById("techModalPrice").textContent = `Prezzo stimato: € ${part.price.toFixed(2)}`;
    document.getElementById("techModalOfficialLink").href = part.tamiyaUrl;

    // Specs table
    const specsTable = document.getElementById("techModalSpecsTable");
    if (specsTable) {
      specsTable.innerHTML = Object.entries(part.specs).map(([k, v]) => `
        <tr>
          <td class="text-muted fw-bold" style="width: 35%;">${k}</td>
          <td class="text-white">${v}</td>
        </tr>
      `).join("");
    }

    // Category Legality breakdown list
    const legalityList = document.getElementById("techModalLegalityList");
    if (legalityList) {
      legalityList.innerHTML = Object.values(categoriesData).map(cat => {
        const isLegal = part.allowedCategories.includes(cat.id);
        const note = part.rulesNotes?.[cat.id] || (isLegal ? "Ammesso senza limitazioni." : "Non ammesso in questa categoria.");
        return `
          <div class="p-2 rounded bg-dark border ${isLegal ? 'border-success border-opacity-50' : 'border-danger border-opacity-25'} d-flex align-items-start gap-2">
            <span class="badge ${isLegal ? 'bg-success' : 'bg-danger'} mt-1 font-heading">${cat.badge}</span>
            <div class="small">
              <strong class="${isLegal ? 'text-success' : 'text-danger'}">${isLegal ? 'OMOLOGATO' : 'VIETATO'}</strong>
              <div class="text-muted">${note}</div>
            </div>
          </div>
        `;
      }).join("");
    }

    techDetailsModal.show();
  }

  // =========================================================================
  // FILTER BAR EVENT LISTENERS
  // =========================================================================
  function updateFilterPills() {
    const pillsContainer = document.getElementById("componentTypeFilterContainer");
    if (!pillsContainer) return;
    pillsContainer.querySelectorAll(".filter-pill-btn").forEach(btn => {
      const type = btn.getAttribute("data-type");
      btn.classList.toggle("active", type === state.currentTypeFilter);
    });
  }

  document.getElementById("componentTypeFilterContainer")?.addEventListener("click", (e) => {
    const btn = e.target.closest(".filter-pill-btn");
    if (!btn) return;
    state.currentTypeFilter = btn.getAttribute("data-type");
    updateFilterPills();
    renderComponentsGrid();
  });

  document.getElementById("legalOnlyToggle")?.addEventListener("change", (e) => {
    state.legalOnlyFilter = e.target.checked;
    renderComponentsGrid();
    showToast(state.legalOnlyFilter ? "Filtro: Mostrati solo i pezzi 100% legali" : "Filtro: Mostrati tutti i componenti del catalogo", "bi-funnel-fill");
  });

  document.getElementById("componentSearchInput")?.addEventListener("input", (e) => {
    state.searchQuery = e.target.value;
    renderComponentsGrid();
  });

  document.getElementById("navbarCategorySelect")?.addEventListener("change", (e) => {
    setCategory(e.target.value);
  });

  // Action Buttons in Summary (Copy, Print, Clear)
  document.getElementById("btnCopyBom")?.addEventListener("click", () => {
    const selectedParts = Array.from(state.selectedPartIds).map(id => componentsData.find(p => p.id === id)).filter(Boolean);
    if (selectedParts.length === 0) {
      showToast("Nessun componente nel build da copiare!", "bi-exclamation-circle", "text-warning");
      return;
    }

    const cat = categoriesData[state.currentCategory];
    const totalPrice = selectedParts.reduce((s, p) => s + p.price, 0);

    let text = `========================================\n`;
    text += `TAMIYA MINI 4WD ITALIA - BUILD CONFORME\n`;
    text += `Categoria: ${cat.name} (${cat.badge})\n`;
    text += `Data: ${new Date().toLocaleDateString('it-IT')}\n`;
    text += `Totale Componenti: ${selectedParts.length}\n`;
    text += `Costo Stimato: € ${totalPrice.toFixed(2)}\n`;
    text += `========================================\n\n`;

    selectedParts.forEach((p, idx) => {
      text += `${idx + 1}. [Item #${p.itemNumber}] ${p.name}\n`;
      text += `   Categoria: ${p.category.toUpperCase()} | Prezzo: € ${p.price.toFixed(2)}\n`;
      text += `   Link Tamiya: ${p.tamiyaUrl}\n\n`;
    });

    navigator.clipboard.writeText(text).then(() => {
      showToast("Lista ricambi copiata negli appunti! Pronta per acquisto o condivisione.", "bi-clipboard-check", "text-success");
    }).catch(() => {
      showToast("Impossibile copiare negli appunti automaticamente.", "bi-x-circle", "text-danger");
    });
  });

  document.getElementById("btnPrintBom")?.addEventListener("click", () => {
    window.print();
  });

  document.getElementById("btnClearBom")?.addEventListener("click", () => {
    if (state.selectedPartIds.size === 0) return;
    if (confirm("Vuoi davvero svuotare la configurazione corrente?")) {
      state.selectedPartIds.clear();
      renderComponentsGrid();
      updateSummaryAndLegality();
      showToast("Configurazione svuotata.", "bi-trash3", "text-info");
    }
  });

  document.getElementById("btnLoadPresetDirect")?.addEventListener("click", () => {
    loadPreset(state.currentCategory);
  });



  // Auto-close mobile navbar on link click
  const navContent = document.getElementById("navContent");
  if (navContent) {
    navContent.querySelectorAll("a.nav-link, a.btn").forEach(link => {
      link.addEventListener("click", () => {
        const bsCollapse = bootstrap.Collapse.getInstance(navContent);
        if (bsCollapse && window.innerWidth < 992) {
          bsCollapse.hide();
        }
      });
    });
  }

  // Floating Mobile Dock Action: Scroll to summary smoothly
  const floatingGoToSummary = document.getElementById("floatingGoToSummaryBtn");
  if (floatingGoToSummary) {
    floatingGoToSummary.addEventListener("click", (e) => {
      const summarySec = document.getElementById("summarySection");
      if (summarySec) {
        e.preventDefault();
        summarySec.scrollIntoView({ behavior: "smooth" });
      }
    });
  }

  // =========================================================================
  // INITIAL BOOTSTRAP
  // =========================================================================
  renderCategoryCards();
  renderCategoryGuide();
  renderPaddockTips();
  renderComponentsGrid();
  updateSummaryAndLegality();
});
