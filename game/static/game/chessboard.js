(function () {

    function Chessboard(elementId, cfg) {

        cfg = cfg || {};

        const boardEl = document.getElementById(elementId);
        if (!boardEl) {
            console.error(`Chessboard: element "${elementId}" not found`);
            return;
        }

        const boardSize = cfg.width || 400;

        // Default piece theme (your HTML overrides it)
        cfg.pieceTheme = cfg.pieceTheme || "chess_pieces/{piece}.png";

        function getPieceUrl(piece) {
            if (!cfg.pieceTheme) return "";
            if (typeof cfg.pieceTheme === "function") {
                try { return cfg.pieceTheme(piece); }
                catch (err) { console.error(err); return ""; }
            }
            let tpl = String(cfg.pieceTheme);
            return tpl
                .replace("%7Bpiece%7D", piece)
                .replace("{piece}", piece);
        }

        boardEl.style.cssText = `
            position: relative;
            width: ${boardSize}px;
            height: ${boardSize}px;
            user-select: none;
        `;

        const files = "abcdefgh";
        const ranks = "87654321";
        const squareSize = boardSize / 8;

        const squares = new Map();
        let position = {};
        let selectedSquare = null;
        let legalMoves = [];
        let sourceSquare = null;

        // =========================================
        // ADDED: FIX – missing function
        // =========================================
        function onMouseDown(e) {
            const sq = e.target.dataset.square || e.target.parentElement.dataset.square;
            if (sq) sourceSquare = sq;
        }

        // =========================================
        // INIT BOARD
        // =========================================
        function initBoard() {
            boardEl.innerHTML = "";
            squares.clear();

            for (let r = 0; r < 8; r++) {
                for (let f = 0; f < 8; f++) {

                    const squareName = files[f] + ranks[r];
                    const light = (r + f) % 2 === 0;

                    const square = document.createElement("div");
                    square.className = "chess-square";
                    square.dataset.square = squareName;

                    square.style.cssText = `
                        width: ${squareSize}px;
                        height: ${squareSize}px;
                        position: absolute;
                        left: ${f * squareSize}px;
                        top: ${r * squareSize}px;
                        background-color: ${light ? "#eeeed2" : "#769656"};
                        border: 1px solid rgba(0,0,0,0.1);
                        transition: background-color .15s;
                    `;

                    square.addEventListener("mousedown", onMouseDown);
                    square.addEventListener("click", () => onSquareClick(squareName));
                    square.addEventListener("dragover", e => e.preventDefault());
                    square.addEventListener("drop", onDrop);

                    squares.set(squareName, square);
                    boardEl.appendChild(square);
                }
            }
        }

        // =========================================
        // RENDER POSITION
        // =========================================
        function renderPosition() {
            squares.forEach(sq => sq.innerHTML = "");

            for (const sq in position) {
                const piece = position[sq];
                const squareEl = squares.get(sq);
                if (!squareEl) continue;

                const img = document.createElement("img");
                img.className = "chess-piece";
                img.src = getPieceUrl(piece);
                img.draggable = true;
                img.dataset.square = sq;

                img.style.cssText = `
                    width: 100%;
                    height: 100%;
                    position: absolute;
                    top: 0;
                    left: 0;
                    cursor: grab;
                    user-select: none;
                `;

                img.addEventListener("dragstart", onDragStart);
                img.addEventListener("dragend", onDragEnd);

                squareEl.appendChild(img);
            }
        }

        // =========================================
        // CLICK-TO-MOVE
        // =========================================
        function onSquareClick(square) {
            if (!selectedSquare) {
                if (position[square]) {
                    selectedSquare = square;
                    showLegalMoves(square);
                }
                return;
            }

            if (square === selectedSquare) {
                clearHighlights();
                selectedSquare = null;
                return;
            }

            if (legalMoves.includes(square)) {
                makeMove(selectedSquare, square);
            } else {
                selectedSquare = square;
                showLegalMoves(square);
            }
        }

        // =========================================
        // DRAG EVENTS
        // =========================================
        function onDragStart(e) {
            sourceSquare = e.target.dataset.square;
            selectedSquare = sourceSquare;

            if (cfg.onShowMoves) legalMoves = cfg.onShowMoves(sourceSquare);
            highlightMoves();

            e.dataTransfer.setData("text/plain", sourceSquare);
        }

        function onDragEnd(e) {
            clearHighlights();
        }

        function onDrop(e) {
            e.preventDefault();
            const targetSquare =
                e.target.dataset.square ||
                e.target.parentElement.dataset.square;

            if (!targetSquare) return;

            makeMove(sourceSquare, targetSquare);
        }

        // =========================================
        // MOVE HIGHLIGHTING
        // =========================================
        function showLegalMoves(square) {
            clearHighlights();
            if (cfg.onShowMoves) legalMoves = cfg.onShowMoves(square);
            highlightMoves();
        }

        function highlightMoves() {
            legalMoves.forEach(sq => {
                const el = squares.get(sq);
                if (el) el.style.boxShadow = "inset 0 0 10px rgba(239, 9, 9, 0.4)";
            });
        }

        function clearHighlights() {
            squares.forEach((el, sq) => {
                const f = sq.charCodeAt(0) - 97;
                const r = 8 - parseInt(sq[1]);
                const light = (f + r) % 2 === 0;
                el.style.backgroundColor = light ? "#eeeed2" : "#769656";
                el.style.boxShadow = "none";
            });
            legalMoves = [];
        }

        // =========================================
        // MAKE MOVE
        // =========================================
        function makeMove(from, to) {
            const result = cfg.onDrop ? cfg.onDrop(from, to) : true;

            if (!result || result === "snapback") {
                clearHighlights();
                renderPosition();
                return;
            }

            if (typeof cfg.getPosition === "function") {
                position = JSON.parse(JSON.stringify(cfg.getPosition()));
            }

            clearHighlights();
            selectedSquare = null;
            renderPosition();
        }

        // =========================================
        // PUBLIC API
        // =========================================
        initBoard();

        return {
            setPosition(newPos) {
                position = JSON.parse(JSON.stringify(newPos));
                renderPosition();
            },
            getPosition() {
                return JSON.parse(JSON.stringify(position));
            },
            move(from, to) {
                makeMove(from, to);
            }
        };
    }

    window.Chessboard = Chessboard;

})();
